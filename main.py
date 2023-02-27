from src.utils import get_create_data_paths
from src.dataset import get_cache_data
from src.features import write_feature_vectors_dict
from src.visualization import write_dimension_reduction_viz
from src.gbr import gbr_model
from pathlib import Path


def run_pipeline():
    # setup and paths
    PATH_BASE = Path("data").expanduser()
    path_raw, path_features, path_output = get_create_data_paths(PATH_BASE)

    # ingest and preprocess raw data
    outpatient = get_cache_data("Outpatient", path_raw)

    # feature extraction, initial TFIDF vectors
    feature_vectors_dict = write_feature_vectors_dict(outpatient, path_features)

    # dimensionality reduction
    list_features = ["DGNS_CD", "HCPCS_CD"]
    write_dimension_reduction_viz(
        path_output, list_features, feature_vectors_dict, [3, 157, 482, 619]
    )

    # supervised learning and prediction
    path_result = path_output.joinpath("PCA_FinalData_GBRModel.csv")
    gbr_model(
        raw_data=outpatient,
        feature_vectors_dict=feature_vectors_dict,
        path_output=path_result,
    )


if __name__ == "__main__":
    run_pipeline()
