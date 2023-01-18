import urllib.request
import zipfile
import pandas as pd
from io import StringIO
import logging

logging.basicConfig(level=logging.INFO)

def get_inpatient():
    INPATIENT_BASE = "https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Inpatient_Claims_Sample_"
    df = pd.DataFrame()

    for i in range(1, 21):
        logging.info(f"Fetching inpatient file {i}...")
        url = f"{INPATIENT_BASE}{i}.zip"
        filehandle, _ = urllib.request.urlretrieve(url)
        zip = zipfile.ZipFile(filehandle, "r")
        first_file = zip.namelist()[0]
        file = zip.open(first_file)
        content = file.read()
        s = str(content, "utf-8")
        data = StringIO(s)
        _df = pd.read_csv(data)
        df = pd.concat([df, _df])
    return df

def get_outpatient():
    INPATIENT_BASE = "https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/Downloads/DE1_0_2008_to_2010_Outpatient_Claims_Sample_"
    df = pd.DataFrame()

    for i in range(1, 21):
        logging.info(f"Fetching outpatient file {i}...")
        url = f"{INPATIENT_BASE}{i}.zip"
        filehandle, _ = urllib.request.urlretrieve(url)
        zip = zipfile.ZipFile(filehandle, "r")
        first_file = zip.namelist()[0]
        file = zip.open(first_file)
        content = file.read()
        s = str(content, "utf-8")
        data = StringIO(s)
        _df = pd.read_csv(data)
        df = pd.concat([df, _df])
    return df

