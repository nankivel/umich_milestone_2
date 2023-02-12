import urllib.request
import zipfile
import pandas as pd
from io import StringIO
import os
import logging
import pathlib

logging.basicConfig(level=logging.INFO)


def get_cache_data(
    dataset, local_cache_raw=pathlib.Path(os.path.join("data", "raw")).expanduser()
):
    os.makedirs(local_cache_raw, exist_ok=True)
    dataset = dataset.title()
    local_cache_path = pathlib.Path(
        os.path.join(local_cache_raw, f"{dataset}.pkl")
    ).expanduser()
    if read_pickle_or_none(local_cache_path) is None:
        df = get_data(dataset)
        logging.info(f"Writing data to local cache file {local_cache_path}")
        df.to_pickle(local_cache_path)
    else:
        logging.info(f"Reading local cache file {local_cache_path}")
        df = pd.read_pickle(local_cache_path)
    return df


def get_data(dataset):
    """
    download, concat and return df of specified dataset
    parameters
    dataset: ["Inpatient", "Outpatient]
    """
    base_url = f"https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_{dataset}_Claims_Sample_"
    df = pd.DataFrame()
    for i in range(1, 21):
        logging.info(f"Fetching file {dataset} {i}...")
        url = f"{base_url}{i}.zip"
        file, _ = urllib.request.urlretrieve(url)
        _df = read_from_zip(file)
        df = pd.concat([df, _df])
    # convert date fields to datetime type
    for c in [c for c in df.columns if "_DT" in c]:
        df[c] = pd.to_datetime(df[c])
    # convert amount fields to float type
    for c in [c for c in df.columns if "_AMT" in c]:
        df[c] = df[c].astype(float)
    return df


def read_from_zip(file):
    zip = zipfile.ZipFile(file, "r")
    first_file = zip.namelist()[0]
    file = zip.open(first_file)
    content = file.read()
    s = str(content, "utf-8")
    data = StringIO(s)
    return pd.read_csv(data, dtype=str)


def read_pickle_or_none(FILE) -> pd.DataFrame:
    if os.path.isfile(FILE):
        result = pd.read_pickle(FILE)
    else:
        result = None
    return result


get_cache_data("Inpatient")
get_cache_data("Outpatient")
