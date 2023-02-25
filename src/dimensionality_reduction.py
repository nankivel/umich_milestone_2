import numpy as np
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from scipy.sparse import hstack

## input is a list of features from the nested dictionary that Taylor's code will spit out. The keys in this dictionary are associated with sparse matrices ##
## If the length of the input is greater than one, the function will do an hstack with those feats and their respective sparse matrices. If not the code    ##
## will simply take the input and run it through the SVD model to return a tuple with the matrix representation of the desired feature set along with the   ##
## Summation of the explained variation ratio array, along with a graph to show how the components are interacting to make-up total explainability. If the  ##
## If the hstack needs to be performed, then it will happen before the SVD model runs and render the above just the same.                                   ##


def SVD_encoder(list_features, feature_vectors_dict: str, n_components: int = 2):
    """
    Dimensionality reduction of the sparce matrices features
    Parameters:
        list_features: list of features to use
        feature_vectors_dict: pickled dictionary of features
        n_components: desired dimensionality of the output data
    Returns:
        result: reduced version of input features, dense array
        plt: matplotlib figure for visualizing explained variance
    """

    num_features = len(input)
    with open(feature_vectors_dict, "rb") as handle:
        masterfeatdict = pickle.load(handle)

    if num_features == 1:
        stack = masterfeatdict(list_features[0])
    else:
        list_array = []
        for i in range(0, num_features):
            list_array.append(masterfeatdict[list_features[i]])
        stack = hstack(list_array)

    svd = TruncatedSVD(n_components=n_components, random_state=42)
    result = svd.fit_transform(stack)
    explained_variance = svd.explained_variance_ratio_
    explained_variance_cumsum = np.cumsum(explained_variance)

    plt.bar(
        range(0, len(explained_variance)),
        explained_variance,
        alpha=0.5,
        align="center",
        label="Individual explained variance",
    )
    plt.step(
        range(0, len(explained_variance_cumsum)),
        explained_variance_cumsum,
        where="mid",
        label="Cumulative explained variance",
    )
    plt.ylabel(f"Explained variance ratio: {round(explained_variance.sum(),2)}")
    plt.xlabel(f"Components: {n_components}")
    plt.title(f'Features: {"|".join(list_features)}')
    plt.legend(loc="best")
    plt.tight_layout()

    return result, plt
