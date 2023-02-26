from src.dimensionality_reduction import SVD_encoder
import plotly.graph_objects as go
import logging
import pickle

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def write_dimension_reduction_viz(
    experiments_output_path,
    list_features,
    feature_vectors_dict,
    component_range=range(3, 10),
):
    for c in component_range:
        svd_explained_variance_path = experiments_output_path.joinpath(
            f"{c}_components.png"
        )
        svd_components_path = experiments_output_path.joinpath(f"{c}_components.pkl")

        logging.info("Performing SVD dimensionality reduction...")
        reduced, plot = SVD_encoder(list_features, feature_vectors_dict, c)

        logging.info(
            f"Writing explained variance plots to {svd_explained_variance_path}..."
        )
        plot.savefig(svd_explained_variance_path)

        logging.info(f"Writing SVD features to {svd_components_path}...")
        with open(svd_components_path, "wb") as f:
            pickle.dump(reduced, f)

        if c == 3:
            svd_3d_html_path = experiments_output_path.joinpath(f"{c}_components.html")
            logging.info(
                f"Writing HTML 3D Scatterplot of SVD components to {svd_3d_html_path}"
            )
            visualize_components3d(reduced).write_html(svd_3d_html_path)


def visualize_components3d(c):
    transposed = c.T
    x, y, z = transposed[0], transposed[1], transposed[2]
    fig = go.Figure(
        data=[
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(size=1, color="black", opacity=0.2),
            )
        ]
    )
    fig.update_layout(width=900, height=1000)
    return fig
