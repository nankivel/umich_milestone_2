import pandas as pd
import os


def read_pickle_or_none(FILE) -> pd.DataFrame:
    if os.path.isfile(FILE):
        result = pd.read_pickle(FILE)
    else:
        result = None
    return result


def get_create_data_paths(base_data_path):
    for dir in ["raw", "features", "experiments"]:
        base_data_path.joinpath(dir).mkdir(parents=True, exist_ok=True)

    raw_data_path = base_data_path.joinpath("raw").joinpath("outpatient.pkl")
    feature_vectors_dict_path = base_data_path.joinpath("features").joinpath(
        "feature_vectors_dictionary-truncated.pkl"
    )
    experiments_output_path = base_data_path.joinpath("experiments").joinpath(
        "dimensionality_reduction"
    )
    experiments_output_path.mkdir(parents=True, exist_ok=True)
    return raw_data_path, feature_vectors_dict_path, experiments_output_path
