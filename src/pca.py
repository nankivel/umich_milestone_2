from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import pickle
from sklearn.decomposition import TruncatedSVD
import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix, hstack

## input is a list of features from the nested dictionary that Taylor's code will spit out. The keys in this dictionary are associated with sparse matrices ##
## If the length of the input is greater than one, the function will do an hstack with those feats and their respective sparse matrices. If not the code    ##
## will simply take the input and run it through the SVD model to return a tuple with the matrix representation of the desired feature set along with the   ##
## Summation of the explained variation ratio array, along with a graph to show how the components are interacting to make-up total explainability. If the  ##
## If the hstack needs to be performed, then it will happen before the SVD model runs and render the above just the same.                                   ##


def PCA_encoder(input, x):
    with open("data/features/feature_vectors_dictionary.pkl", "rb") as handle:
        masterfeatdict = pickle.load(handle)
    if len(input) == 4:
        a = masterfeatdict[input[0]]
        b = masterfeatdict[input[1]]
        c = masterfeatdict[input[2]]
        d = masterfeatdict[input[3]]
        stack = hstack([a, b, c, d])
    elif len(input) == 3:
        a = masterfeatdict[input[0]]
        b = masterfeatdict[input[1]]
        c = masterfeatdict[input[2]]
        stack = hstack([a, b, c])
    elif len(input) == 2:
        a = masterfeatdict[input[0]]
        b = masterfeatdict[input[1]]
        stack = hstack([a, b])
    else:
        stack = masterfeatdict[input[0]]

    encodedfeats = TruncatedSVD(n_components=x)

    encodedfeats_fit = encodedfeats.fit_transform(stack)

    exp_var_pca = encodedfeats.explained_variance_ratio_

    cum_sum_eigenvalues = np.cumsum(exp_var_pca)
    #

    # Create the visualization plot
    #
    plt.bar(
        range(0, len(exp_var_pca)),
        exp_var_pca,
        alpha=0.5,
        align="center",
        label="Individual explained variance",
    )
    plt.step(
        range(0, len(cum_sum_eigenvalues)),
        cum_sum_eigenvalues,
        where="mid",
        label="Cumulative explained variance",
    )
    plt.ylabel("Explained variance ratio")
    plt.xlabel("Principal components")
    plt.legend(loc="best")
    plt.tight_layout()
    plt.show()

    return encodedfeats_fit, exp_var_pca.sum()