UMich Milestone 2 Team Project

[Skyler Young](https://github.com/skyyy1234), [Taylor Druhot](https://github.com/twdruhot), [Josh Nankivel](https://github.com/nankivel)

 
Milestone 2 Project

Introduction

How much will a trip to the hospital cost you? That is one of the questions we are seeking to answer for our project. This is an intriguing problem and one that a lot of Americans ask themselves before receiving their claim/bill in the mail from a medical encounter. 

We are going to attempt to utilize a publicly available dataset offered by CMS (Center for Medicare and Medicaid Services) that contains Inpatient and Outpatient medical claims data from Medicare beneficiaries. These datasets have relevant features such as: diagnosis, procedures, and price (among other things) that should make for an intriguing project!

Dataset 

We were able to find another project that used this dataset for a completely different task (hospital readmissions involving pulmonary disorders) (see link below). To our knowledge, we are engaging in a unique exercise that has not been attempted or has not been made publicly available. 

[Dataset](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF) | [Existing Project](https://www.ijert.org/comparison-of-different-machine-learning-models-for-predicting-chronic-obstructive-pulmonary-disorder-hospital-readmissions)

Unsupervised Task

Dataset (see Outpatient and Inpatient) [Dataset](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF)

Due to the high dimensionality presented by utilizing diagnosis codes and procedure codes, we will seek to utilize Unsupervised learning techniques to reduce dimensionality for our Supervised tasks.

Upon encoding the diagnosis codes and procedures with either one-hot encoding and/or TF-IDF methods, we will seek to reduce dimensionality with an Unsupervised model such as PCA or SVD. These Unsupervised methods will bring the dimensionality down significantly, while still capturing the salient feature exhaust.

For Unsupervised tasks, visualizing results is a good way of understanding how well the Unsupervised model performed in finding structure within the dataset. For this task, we will utilize either Plotly (3D scatter plot) or the Tensorflow Embedding Projector. Both of these tools are good for visualizing vectors in 3D and help understand if the model was able to find coherent structures.

Another idea we have is to perhaps deploy a DBSCAN or k-Means Unsupervised cluster model on top of the PCA vectors/one-hot vectors to further compress features into actual clusters. Utilizing the cluster labels as an all encompassing feature for downstream tasks. If we choose to go this route, depending on the cluster model we choose, we will need to evaluate the model differently. For example, silhouette score for k-Means works well for determining the optimal number of clusters, as well as utilizing the elbow-method/inertia. k-Means has of course one main hyperparameter which is k (number of clusters). For DBSCAN, evaluating the results that make it to each cluster is a great way to evaluate that particular model. DBSCAN has two important hyperparameters to set which are: epsilon and min_samples. Epsilon is a hyperparameter that sets the boundary distance to make it into a cluster and min_samples is a hyperparameter that tells the model how many samples it takes to make a cluster. 

Supervised Task

Dataset (see Outpatient and Inpatient) [Dataset](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/SynPUFs/DE_Syn_PUF)

As stated in the introduction, our main Supervised task will be to try to fit a model utilizing claim features in order to make a prediction on price. We plan to utilize a gradient tree boosting, stochastic gradient descent, and elastic-net model to create our models. The reasoning behind picking these models opposed to other supervised regressors is that the features of our dataset are sparse but highly correlated. 

We plan to train our models using both the base data, and reduced data from the unsupervised portion of our project to see which models perform best. To evaluate our models we plan to use the R2 score and mean squared error. The R2 score will give us an indication of how well our model is fit overall while the mean squared error should give us an indication of the performance of our models particularly in relation to differences in outlier actuals and predictions. To visualize our results we will plot our evaluation metrics by model alongside those same metrics by dummy models.

Team Planning

Skyler - Data Procurement/Wrangling, Data Visualization, Unsupervised Model, Data Exploration

Taylor - Data Procurement/Wrangling, Data Visualization, Supervised Model, Data Exploration

Josh - Assist Skyler and Taylor with supervised/unsupervised tasks, Data Visualization and Report Write-up
