from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
from joblib import parallel_backend
import xgboost as xgb
import pandas as pd

# import warnings
# warnings.filterwarnings("ignore")
import numpy as np
import itertools
from tqdm import tqdm
from scipy import sparse


def run_model(X, y, model, grid, feature_names, outpatient):
    ### Runs the model and returns MSE and R2 values and corresponding data as a dataframe

    ### Takes in four arugments
    ### X is the features to that model will be trained on as a sparse matrix
    ### y is the scalar that is to be predicted as a list
    ### model is the regression model as a model object
    ### grid is a dictionary of model hyperparameters

    ### returns a dataframe of results from the grid search

    scoring = {
        "mean_squared_error": make_scorer(mean_squared_error),
        "r2_score": make_scorer(r2_score),
    }
    with parallel_backend("threading", n_jobs=2):
        grid_model = GridSearchCV(
            model,
            grid,
            scoring=scoring,
            refit="r2_score",
            return_train_score=True,
            error_score="raise",
        ).fit(X.todense(), y)

    preds = grid_model.predict(X.todense())

    df = outpatient.copy()

    df["predictions"] = preds

    return df


def iterate_feature_sets(model, feature_dict, grid, feature_sets, outpatient):
    ### Creates and runs the specified model with each comboniation of features sets from 1 to k length features and stores the results of the models into a dictionary

    ### Takes in four arguments
    ### model is the regression model as a model object
    ### feature_dict is the dictionary of feature sets
    ### grid is a dictionary of model hyperparameters
    ### feature_sets dicates how what feature sets will be returned, a list of list of strings corresponding to the keys in the dictionary
    ### (continued) all would return all combinations for 1 through k, where  k is the number of keys in feature_dict

    ### returns a dictionary of results

    results = {}

    for feature_list in feature_sets:
        if feature_list == "all":
            for n_met in tqdm(range(len(feature_dict))):
                for met_set in list(
                    itertools.combinations(feature_dict.keys(), n_met + 1)
                ):
                    for n_met_set in range(len(met_set)):
                        if n_met_set == 0:
                            X = feature_dict[met_set[n_met_set]]
                        else:
                            X = sparse.hstack(
                                (X, feature_dict[met_set[n_met_set]]), format="csr"
                            )
                    answer = run_model(
                        X,
                        outpatient["CLM_PMT_AMT"].values.tolist(),
                        model,
                        grid,
                        met_set,
                        outpatient,
                    )
                    results[met_set] = answer

        else:
            X = None
            Name = ()
            for i in feature_list:
                if X == None:
                    X = feature_dict[i]
                    Name += (i,)
                else:
                    X = sparse.hstack((X, feature_dict[i]), format="csr")
                    Name += (i,)
            answer = run_model(
                X,
                outpatient["CLM_PMT_AMT"].values.tolist(),
                model,
                grid,
                feature_list,
                outpatient,
            )
            results[Name] = answer

    return results


def write_results(results_dict, filename):
    ### Takes in two arguements
    ### results_dict is the dictionary of feature sets
    ### file name is the wanted file name as a string

    ### Returns None, but writes a file to the current directory

    df = pd.DataFrame()

    for r_key in results_dict.keys():
        temp_df = results_dict[r_key]
        temp_df["features"] = str(r_key)
        df = pd.concat((df, temp_df), ignore_index=True)

    df.to_csv(filename)

    return None
