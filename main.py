from src.dataset import get_cache_data
from src.features import write_feature_vectors_dict
from src.dimensionality_reduction import SVD_encoder
from src.visualization import visualize_components3d
import pickle
from pathlib import Path


BASE_DATA_PATH = Path("data").expanduser()

# create data subfolders if they don't already exist
for dir in ["raw", "features", "experiments"]:
    BASE_DATA_PATH.joinpath(dir).mkdir(parents=True, exist_ok=True)


raw_data_path = BASE_DATA_PATH.joinpath("raw").joinpath("outpatient.pkl")
feature_vectors_dict_path = BASE_DATA_PATH.joinpath("features").joinpath(
    "feature_vectors_dictionary-truncated.pkl"
)
experiments_output_path = BASE_DATA_PATH.joinpath("experiments").joinpath(
    "dimensionality_reduction"
)

outpatient = get_cache_data("Outpatient", raw_data_path)
feature_vectors_dict = write_feature_vectors_dict(outpatient, feature_vectors_dict_path)
list_features = ["State", "DGNS_CD", "PRDCR_CD", "HCPCS_CD"]

for c in range(3, 7):
    reduced, plot = SVD_encoder(list_features, feature_vectors_dict, c)
    plot.savefig(experiments_output_path.joinpath(f"{c}_components.png"))
    with open(experiments_output_path.joinpath(f"{c}_components.pkl"), "wb") as f:
        pickle.dump(reduced, f)
    visualize_components3d(reduced)
