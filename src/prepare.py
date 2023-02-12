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

if len(sys.argv) != 3:
    sys.stderr.write("Arguments error. Usage:\n")
    sys.stderr.write("\tpython prepare.py data-file-inpatient data-file-outpatient\n")
    sys.exit(1)

try:
    logging.info("Reading and concatenating input data files...")
    df_raw = pd.concat([pd.read_pickle(sys.argv[1]), pd.read_pickle(sys.argv[2])])
    logging.info("Complete!")
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
