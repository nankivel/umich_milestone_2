from sklearn.ensemble import HistGradientBoostingRegressor
from .dimensionality_reduction import SVD_encoder
from .supervised import iterate_feature_sets, write_results
import yaml


def gbr_model(raw_data, feature_vectors_dict, path_output):
    (
        feature_vectors_dict["SVD-HCPCS_CD"],
        plot_svd_explained_variance_hcpcs_cd,
    ) = SVD_encoder(["HCPCS_CD"], feature_vectors_dict, 619)
    (
        feature_vectors_dict["SVD-DGNS_CD"],
        plot_svd_explained_variance_dgns_cd,
    ) = SVD_encoder(["DGNS_CD"], feature_vectors_dict, 619)
    list_svd_plots = [
        plot_svd_explained_variance_hcpcs_cd,
        plot_svd_explained_variance_dgns_cd,
    ]

    final_feature_set = yaml.safe_load(open("params.yaml"))["features"][
        "final_feature_set"
    ]
    random_seed = yaml.safe_load(open("params.yaml"))["general"]["random_seed"]
    grid_dict = {
        "learning_rate": [0.25],
        "max_iter": [200],
        # wanted to go a little higher on leaf nodes since there seemed to be more to gain
        "max_leaf_nodes": [10],
        "max_depth": [18]
        # results were inconclusive for minimum samples, going to leave as default
    }

    GBRModel = HistGradientBoostingRegressor(random_state=random_seed)
    results_dict = iterate_feature_sets(
        GBRModel, feature_vectors_dict, grid_dict, final_feature_set, raw_data
    )
    write_results(results_dict, path_output)
    return list_svd_plots
