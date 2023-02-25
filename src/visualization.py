import plotly.graph_objects as go
import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)


def visualize_components3d(c):
    logging.info("Visualizing components in 3D...")
    x, y, z = c[0], c[1], c[2]
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="markers")])
    fig.update_layout(width=900, height=1000)
    fig.show()
