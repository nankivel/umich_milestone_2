import plotly.graph_objects as go


def visualize_components3d(c):
    x, y, z = c[0], c[1], c[2]
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode="markers")])
    fig.update_layout(width=900, height=1000)
    fig.show()
