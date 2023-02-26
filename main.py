from src.utils import get_create_data_paths
from src.dataset import get_cache_data
from src.features import write_feature_vectors_dict
from src.visualization import write_dimension_reduction_viz
from pathlib import Path


def pipeline():
    # setup and paths
    BASE_DATA_PATH = Path("data").expanduser()
    path_raw, path_features, path_experiments = get_create_data_paths(BASE_DATA_PATH)

    # ingest and preprocess raw data
    outpatient = get_cache_data("Outpatient", path_raw)

    # feature extraction, initial TFIDF vectors
    feature_vectors_dict = write_feature_vectors_dict(outpatient, path_features)

    # supverised learning and prediction without dimensionality reduction
    # TODO: incorporate Taylor's work without SVD here

    # dimensionality reduction
    list_features = ["State", "DGNS_CD", "PRDCR_CD", "HCPCS_CD"]
    write_dimension_reduction_viz(path_experiments, list_features, feature_vectors_dict)

    # supervised learning and prediction
    # TODO: incorporate Taylor's work with SVD here


if __name__ == "__main__":
    pipeline()
