import urllib.request
import zipfile
import pandas as pd
from io import StringIO
import os
import logging
import pathlib

logging.basicConfig(level=logging.INFO)


def get_cache_data(dataset, local_cache_path):
    local_cache_path = pathlib.Path(local_cache_path).expanduser()
    if read_pickle_or_none(local_cache_path) is None:
        df = get_data(dataset)
        logging.info(df.shape)
        df_demog = get_data(
            "Demographics",
            fetch_column_list=[
                "DESYNPUF_ID",
                "BENE_BIRTH_DT",
                "BENE_SEX_IDENT_CD",
                "SP_STATE_CODE",
                "BENE_COUNTY_CD",
            ],
        )
        df = df.merge(df_demog, how="left", on="DESYNPUF_ID")
        logging.info(df.shape)
        logging.info(f"Writing data to local cache file {local_cache_path}")
        df.to_pickle(local_cache_path)
    else:
        logging.info(f"Reading local cache file {local_cache_path}")
        df = pd.read_pickle(local_cache_path)
    return df


def get_data(dataset, fetch_count=1, fetch_column_list=None):
    """
    download, concat and return df of specified dataset
    parameters
    dataset: ["Inpatient", "Outpatient","Demographics"]
    """
    base_url = f"https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_{dataset}_Claims_Sample_"

    if dataset == "Demographics":
        base_url = f"https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_Beneficiary_Summary_File_Sample_"

    df = pd.DataFrame()
    for i in range(1, fetch_count + 1):
        logging.info(f"Fetching file {dataset} {i}...")
        url = f"{base_url}{i}.zip"
        file, _ = urllib.request.urlretrieve(url)
        if fetch_column_list is None:
            _df = read_from_zip(file)
        else:
            _df = read_from_zip(file)[fetch_column_list]
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


if __name__ == "__main__":
    get_cache_data("Outpatient", "~/Downloads/outpatient.pkl")
