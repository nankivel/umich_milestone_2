import os
import random
import sys
import yaml
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
import logging
import pathlib

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

params = yaml.safe_load(open("params.yaml"))["prepare"]

if len(sys.argv) != 2:
    logging.info("Arguments error. Usage:\n")
    logging.info("\tpython prepare.py data-file-outpatient\n")
    sys.exit(1)

try:
    logging.info("Reading input data file...")
    df_raw = pd.read_pickle(sys.argv[1])
    logging.info("Complete!")
    df_raw.dropna(subset=["CLM_PMT_AMT"], inplace=True)
    df_raw.dropna(subset=["CLM_FROM_DT", "CLM_THRU_DT"], inplace=True)
    df_raw.dropna(
        subset=[
            "ICD9_PRCDR_CD_1",
            "ICD9_PRCDR_CD_2",
            "ICD9_PRCDR_CD_3",
            "ICD9_PRCDR_CD_4",
            "ICD9_PRCDR_CD_5",
            "ICD9_PRCDR_CD_6",
        ],
        inplace=True,
        how="all",
    )
    df_raw.dropna(
        subset=[
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
        inplace=True,
        how="all",
    )
except Exception as err:
    logging.info(f"Unexpected {err=}, {type(err)=}")

# Test data set split ratio
test_ratio = params["test_ratio"]
random_seed = random.seed(params["random_seed"])

try:
    logging.info(
        f"Splitting into train and test sets with specified test ratio:{test_ratio}, random_seed: {random_seed}"
    )
    train, test = train_test_split(
        df_raw, test_size=test_ratio, random_state=random_seed
    )
    logging.info("Complete!")
except Exception as err:
    logging.info(f"Unexpected {err=}, {type(err)=}")

try:
    logging.info(f"Writing train and test sets to data/prepared/")
    os.makedirs(os.path.join("data", "prepared"), exist_ok=True)
    output_train = pathlib.Path(
        os.path.join("data", "prepared", "train.pkl")
    ).expanduser()
    output_test = pathlib.Path(
        os.path.join("data", "prepared", "test.pkl")
    ).expanduser()

    with open(output_train, "wb") as f:
        pickle.dump(train, f)

    with open(output_test, "wb") as f:
        pickle.dump(test, f)
    logging.info("Complete!")
except Exception as err:
    logging.info(f"Unexpected {err=}, {type(err)=}")
