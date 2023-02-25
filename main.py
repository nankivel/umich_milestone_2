from src.dimensionality_reduction import SVD_encoder
from src.visualization import visualize_components3d
import pickle
from pathlib import Path


list_features = ["State", "DGNS_CD", "PRDCR_CD", "HCPCS_CD"]
feature_vectors_dict = (
    Path("data")
    .expanduser()
    .joinpath("features")
    .joinpath("feature_vectors_dictionary-truncated.txt")
)
experiments_output_path = (
    Path("data")
    .expanduser()
    .joinpath("experiments")
    .joinpath("dimensionality_reduction")
)
experiments_output_path.mkdir(parents=True, exist_ok=True)

for c in range(3, 7):
    reduced, plot = SVD_encoder(list_features, feature_vectors_dict, c)
    plot.savefig(experiments_output_path.joinpath(f"{c}_components.png"))
    with open(experiments_output_path.joinpath(f"{c}_components.pkl"), "wb") as f:
        pickle.dump(reduced, f)
    visualize_components3d(reduced)
