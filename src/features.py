from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
from dataset import get_cache_data
import yaml
import logging
import sys
import pandas as pd

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

params = yaml.safe_load(open("params.yaml"))["features"]

if len(sys.argv) != 2:
    logging.info("Arguments error. Usage:\n")
    logging.info("\tpython features.py file-training-set\n")
    sys.exit(1)

try:
    logging.info("Reading training dataset...")
    train = pd.read_pickle(sys.argv[1])
    logging.info("Training dataset in memory")
except Exception as err:
    logging.info(f"Unexpected {err=}, {type(err)=}")


def isnan(x):
    return x != x


def TFIDF_Matrix(df, columns):
    # Takes in a dataframe, and a list of columns that comprise a "sentence"
    # Returns a TFIDF matrix
    corpus = df[columns].apply(lambda x: x.str.cat(sep=" "), axis=1).dropna().to_list()
    return TfidfVectorizer().fit_transform(corpus).todense()


def Date_Diff(df, columns):
    # Takes in a dataframe, and a list of columns that are a start date and end date
    # Returns the difference between the two dates
    logging.info("Computing claim duration in days...")
    values = df[columns]
    values.insert(
        len(values),
        "date_diff",
        (df[columns[1]] - df[columns[0]]) / np.timedelta64(1, "D"),
    )
    return np.array(values["date_diff"].values.tolist()).reshape(len(values), 1)


def Passthrough(df, columns):
    # Takes in a dataframe, and a list of columns that need to be turned into a list
    # Returns list of values from columns
    return np.array(df[columns].values.tolist())


column_sets_dict = params["column_sets_dict"]

column_sets_matrix_dict = {}
for key, value in column_sets_dict.items():
    if key in [
        "provider",
        "NPI",
        "admit_code",
        "claim_discharge_code",
        "DGNS_CD",
        "PRDCR_CD",
        "HCPCS_CD",
    ]:
        logging.info(f"Generating TFIDF matrix for {key}...")
        column_sets_matrix_dict[key] = TFIDF_Matrix(train, value)
    elif key in ["clm_dates", "admit_dates"]:
        column_sets_matrix_dict[key] = Date_Diff(train, value)
    else:
        column_sets_matrix_dict[key] = Passthrough(train, value)


with open("data/features/feature_vectors_dictionary.pkl", "wb") as f:
    logging.info("Writing feature vectors to pickle file...")
    pickle.dump(column_sets_matrix_dict, f)
