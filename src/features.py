from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
from dataset import get_cache_data
import yaml
import logging
import pathlib
import sys
import pandas as pd

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

params = yaml.safe_load(open("params.yaml"))["features"]


if len(sys.argv) != 2:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython features.py file-training-set\n")
    sys.exit(1)

try:
    logging.info("Reading training set...")
    train = pd.read_pickle(sys.argv[1])
except Exception as err:
    logging.info(f"Unexpected {err=}, {type(err)=}")

column_sets_dict = {
    "clm_dates": ["CLM_FROM_DT", "CLM_THRU_DT"],
    "PRDCR_CD": [
        "ICD9_PRCDR_CD_1",
        "ICD9_PRCDR_CD_2",
        "ICD9_PRCDR_CD_3",
        "ICD9_PRCDR_CD_4",
        "ICD9_PRCDR_CD_5",
        "ICD9_PRCDR_CD_6",
    ],
    "HCPCS_CD": [
        "HCPCS_CD_1",
        "HCPCS_CD_2",
        "HCPCS_CD_3",
        "HCPCS_CD_4",
        "HCPCS_CD_5",
        "HCPCS_CD_6",
        "HCPCS_CD_7",
        "HCPCS_CD_8",
        "HCPCS_CD_9",
        "HCPCS_CD_10",
        "HCPCS_CD_11",
        "HCPCS_CD_12",
        "HCPCS_CD_13",
        "HCPCS_CD_14",
        "HCPCS_CD_15",
        "HCPCS_CD_16",
        "HCPCS_CD_17",
        "HCPCS_CD_18",
        "HCPCS_CD_19",
        "HCPCS_CD_20",
        "HCPCS_CD_21",
        "HCPCS_CD_22",
        "HCPCS_CD_23",
        "HCPCS_CD_24",
        "HCPCS_CD_25",
        "HCPCS_CD_26",
        "HCPCS_CD_27",
        "HCPCS_CD_28",
        "HCPCS_CD_29",
        "HCPCS_CD_30",
        "HCPCS_CD_31",
        "HCPCS_CD_32",
        "HCPCS_CD_33",
        "HCPCS_CD_34",
        "HCPCS_CD_35",
        "HCPCS_CD_36",
        "HCPCS_CD_37",
        "HCPCS_CD_38",
        "HCPCS_CD_39",
        "HCPCS_CD_40",
        "HCPCS_CD_41",
        "HCPCS_CD_42",
        "HCPCS_CD_43",
        "HCPCS_CD_44",
        "HCPCS_CD_45",
    ],
}


def isnan(x):
    return x != x


def TFIDF_Matrix(df, columns):
    # Takes in a dataframe, and a list of columns that comprise a "sentence"
    # Returns a TFIDF matrix

    corpus = []

    if len(columns) > 1:
        values = df[columns].values.tolist()
        for sentence in values:
            s = ""
            for word in sentence:
                if len(s) == 0:
                    if isnan(word):
                        s = "None"
                    else:
                        s = str(word)
                else:
                    if isnan(word):
                        s += "None"
                    else:
                        s += str(word)
            corpus.append(s)

    else:
        values = df[columns].values.tolist()
        for word in values:
            if isnan(word[0]):
                corpus.append("None")
            else:
                corpus.append(word[0])

    return TfidfVectorizer(stop_words=["None"]).fit_transform(corpus).todense()


def Date_Diff(df, columns):
    # Takes in a dataframe, and a list of columns that are a start date and end date
    # Returns the difference between the two dates

    values = df[columns]

    values["date_diff"] = (df[columns[1]] - df[columns[0]]) / np.timedelta64(1, "D")

    return np.array(values["date_diff"].values.tolist()).reshape(len(values), 1)


def Passthrough(df, columns):
    # Takes in a dataframe, and a list of columns that need to be turned into a list
    # Returns list of values from columns

    return np.array(df[columns].values.tolist())


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
        column_sets_matrix_dict[key] = TFIDF_Matrix(train, value)
    elif key in ["clm_dates", "admit_dates"]:
        column_sets_matrix_dict[key] = Date_Diff(train, value)
    else:
        column_sets_matrix_dict[key] = Passthrough(train, value)


with open("data/features/feature_vectors_dictionary.pkl", "wb") as f:
    pickle.dump(column_sets_matrix_dict, f)
