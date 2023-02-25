import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pickle
from .dataset import get_cache_data
import yaml
import pandas as pd
from pathlib import Path
import logging

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

params = yaml.safe_load(open("params.yaml"))["features"]


def isnan(x):
    return x != x


def TFIDF_Matrix_len_char(df, columns, len_char):
    # Takes in a dataframe, and a list of columns that comprise a "sentence" using the first three characters of each word
    # Returns a TFIDF matrix

    corpus = []

    if len(columns) > 1:
        values = df[columns].values.tolist()

        for sentence in values:
            s = ""
            for word in sentence:
                if len(s) == 0:
                    if isnan(word):
                        s = "None, "
                    else:
                        s = (
                            str(word)[:len_char] + " "
                        )  # Add [:3] after str(word) to truncate to the first 3 characters
                else:
                    if isnan(word):
                        s += "None, "
                    else:
                        s += (
                            str(word)[:len_char] + " "
                        )  # Add [:3] after str(word) to truncate to the first 3 characters
            corpus.append(s)

    else:
        values = df[columns].values.tolist()
        for word in values:
            if isnan(word[0]):
                corpus.append("None")
            else:
                corpus.append(
                    word[0][:len_char]
                )  # Add [:3] after word[0] to truncate to the first 3 characters

    a = TfidfVectorizer().fit_transform(corpus)

    return np.nan_to_num(a), np.nan_to_num(np.sum(a, axis=1))


def TFIDF_Matrix(df, columns):
    # Takes in a dataframe, and a list of columns that comprise a "sentence" using the complete "word"
    # Returns a TFIDF matrix

    corpus = []

    if len(columns) > 1:
        values = df[columns].values.tolist()

        for sentence in values:
            s = ""
            for word in sentence:
                if len(s) == 0:
                    if isnan(word):
                        s = "None, "
                    else:
                        s = str(word) + " "
                else:
                    if isnan(word):
                        s += "None, "
                    else:
                        s += str(word) + " "
            corpus.append(s)

    else:
        values = df[columns].values.tolist()
        for word in values:
            if isnan(word[0]):
                corpus.append("None")
            else:
                corpus.append(word[0])

    a = TfidfVectorizer(stop_words=["None"]).fit_transform(corpus)

    return np.nan_to_num(a)


def Date_Year(df, columns):
    df["year"] = pd.DatetimeIndex(df[columns[0]]).year

    return np.nan_to_num(np.array(df["year"].values.tolist()).reshape(len(df), 1))


def Date_Diff(df, columns):
    # Takes in a dataframe, and a list of columns that are a start date and end date
    # Returns the difference between the two dates
    values = df[columns]
    values.insert(
        len(values.columns),
        "date_diff",
        (df[columns[1]] - df[columns[0]]) / np.timedelta64(1, "D"),
    )

    return np.nan_to_num(
        np.array(values["date_diff"].values.tolist()).reshape(len(values), 1)
        / np.array(values["date_diff"].values.tolist())
        .reshape(len(values), 1)
        .max(axis=0)
    )


def Passthrough(df, columns):
    # Takes in a dataframe, and a list of columns that need to be turned into a list
    # Returns list of values from columns

    df[columns[0]] = pd.to_numeric(df[columns[0]], errors="coerce").astype("Int64")

    return np.nan_to_num(np.array(df[columns].values.tolist()))


def write_feature_vectors_dict(raw_data, feature_vectors_dict_path):
    logging.info("Generating features...")
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
            column_sets_matrix_dict[key] = TFIDF_Matrix(raw_data, value)
        elif key in ["clm_dates", "admit_dates"]:
            column_sets_matrix_dict[key] = Date_Diff(raw_data, value)
        else:
            column_sets_matrix_dict[key] = Passthrough(raw_data, value)

    feature_vectors_dict_path = (
        Path("data")
        .expanduser()
        .joinpath("features")
        .joinpath("feature_vectors_dictionary-truncated.pkl")
    )

    with open(feature_vectors_dict_path, "wb") as f:
        logging.info("Writing feature vectors to pickle file...")
        pickle.dump(column_sets_matrix_dict, f)
        logging.info("Complete!")

    return column_sets_matrix_dict
