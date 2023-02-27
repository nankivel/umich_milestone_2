import pandas as pd
import os


def read_pickle_or_none(FILE) -> pd.DataFrame:
    if os.path.isfile(FILE):
        result = pd.read_pickle(FILE)
    else:
        result = None
    return result


def get_create_data_paths(path_base):
    for dir in ["raw", "features", "output"]:
        path_base.joinpath(dir).mkdir(parents=True, exist_ok=True)

    path_raw = path_base.joinpath("raw").joinpath("outpatient.pkl")
    path_features = path_base.joinpath("features").joinpath(
        "feature_vectors_dictionary-truncated.pkl"
    )
    path_output = path_base.joinpath("output")
    return path_raw, path_features, path_output
