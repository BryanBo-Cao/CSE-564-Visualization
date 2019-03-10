'''
Student: Bryan Bo Cao
SBU ID: 112130213
Email: bo.cao.1@stonybrook.edu or boccao@cs.stonybrook.edu

Dataset:
College 777 data points, 18 dimensions
https://vincentarelbundock.github.io/Rdatasets/datasets.html

Reference:
https://getbootstrap.com/docs
https://www.w3schools.com
Flask code base from TA: https://github.com/hawkeye154/d3_flask_tutorial
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html
https://datascience.stackexchange.com/questions/16700/confused-about-how-to-apply-kmeans-on-my-a-dataset-with-features-extracted
https://pythonprogramminglanguage.com/kmeans-elbow-method/
https://datascience.stackexchange.com/questions/16700/confused-about-how-to-apply-kmeans-on-my-a-dataset-with-features-extracted
https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.PCA.html
'''

import json

from flask import Flask, render_template, request, redirect, Response, jsonify
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import decomposition
from sklearn import preprocessing
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def index():

    global df
    df_all_data = df[['Apps','Accept','Enroll', 'Top10perc', 'Top25perc', 'F.Undergrad', 'P.Undergrad', 'Outstate',
    	       'Room.Board', 'Books', 'Personal', 'PhD', 'Terminal', 'S.F.Ratio', 'perc.alumni', 'Expend', 'Grad.Rate']]
    print("df_all_data:")
    print(df_all_data)
    print("Population of df_all_data: %d" % len(df_all_data))
    print("Number of dimension of df_all_data: %d" % len(df_all_data.columns))

    # ======================== Task1 ========================
    # Task 1: data clustering and decimation (30 points)
    # implement random sampling and stratified sampling
    # the latter includes the need for k-means clustering (optimize k using elbow)
    # ======================== Bryan Bo Cao ========================
    # TA mentioned in the post @123 and @124 in Piazza that we can use in-built
    # pandas or sklearn method, so I use them directly for task1.

    # Normalize data
    min_max_scaler = preprocessing.MinMaxScaler()
    np_scaled = min_max_scaler.fit_transform(df_all_data)
    df_all_data_normalized = pd.DataFrame(np_scaled)
    # print("df_all_data_normalized:", df_all_data_normalized)

    # =================== random sampling ====================
    # df_sampled_data = random_sampling(df_all_data)
    df_sampled_data = random_sampling(df_all_data_normalized)

    # ================= stratified sampling ==================
    # df_ss_data = stratified_sampling(df_all_data)
    df_ss_data = stratified_sampling(df_all_data_normalized)

    # ======================== Task2 ========================
    # Task 2: dimension reduction (use decimated data) (30 points)
    # find the intrinsic dimensionality of the data using PCA
    # produce scree plot visualization and mark the intrinsic dimensionality
    # NEW: show the scree plots before/after sampling to assess the bias introduced
    # you could also visualize the before/after sampling data via MDS (see below)
    # obtain the three attributes with highest PCA loadings

    # ================= PCA -- start ==================
    pca = decomposition.PCA(n_components='mle')
    pca_all_data = pca.fit(df_all_data)
    pca_all_data_explained_variance_ratio_ = pca_all_data.explained_variance_ratio_
    print("pca_all_data_explained_variance_ratio_:", pca_all_data_explained_variance_ratio_)
    pca_all_data_singular_values_ = pca_all_data.singular_values_
    print("pca_all_data_singular_values_:", pca_all_data_singular_values_)
    pca_all_data_explained_variance_ratio_ls = pca_all_data_explained_variance_ratio_.tolist()
    pca_all_data_components_ = pca_all_data.components_
    print("pca_all_data_components_: ", pca_all_data_components_)


    pca = decomposition.PCA(n_components='mle')
    pca_sampled_data = pca.fit(df_sampled_data)
    pca_sampled_data_explained_variance_ratio_ = pca_sampled_data.explained_variance_ratio_
    print("pca_sampled_data_explained_variance_ratio_:", pca_sampled_data_explained_variance_ratio_)
    pca_sampled_data_singular_values_ = pca_sampled_data.singular_values_
    print("pca_sampled_data_singular_values_:", pca_sampled_data_singular_values_)
    pca_sampled_data_explained_variance_ratio_ls = pca_sampled_data_explained_variance_ratio_.tolist()
    pca_sampled_data_components_ = pca_sampled_data.components_
    print("pca_sampled_data_components_: ", pca_sampled_data_components_)
    # ================= PCA -- end ==================

    # ====== Compute the three attributes with highest PCA loadings -- start ======
    all_data_attribute_loadings = []
    for j in range(len(pca_all_data_components_[0])):
        attribute_loading = 0
        for i in range(len(pca_all_data_components_)):
            attribute_loading += np.abs(pca_all_data_components_[i][j])
        all_data_attribute_loadings.append(attribute_loading)
    print("all_data_attribute_loadings: ", all_data_attribute_loadings)
    all_data_attribute_loadings_sorted = all_data_attribute_loadings.copy()
    all_data_attribute_loadings_sorted.sort(reverse = True)
    print("all_data_attribute_loadings_sorted: ", all_data_attribute_loadings_sorted)
    top3_attributes_i_all_data = []
    for i in range(3):
        top3_attributes_i_all_data.append(all_data_attribute_loadings.index(all_data_attribute_loadings_sorted[i]))
    print()
    print("top3_attributes_i_all_data: ", top3_attributes_i_all_data)
    print("top 3 attributes with highest PCA loadings for all data:")
    for i in range(3):
        print("    ", df_all_data.columns[top3_attributes_i_all_data[i]])


    sampled_data_attribute_loadings = []
    for j in range(len(pca_sampled_data_components_[0])):
        attribute_loading = 0
        for i in range(len(pca_sampled_data_components_)):
            attribute_loading += np.abs(pca_sampled_data_components_[i][j])
        sampled_data_attribute_loadings.append(attribute_loading)
    print("sampled_data_attribute_loadings: ", sampled_data_attribute_loadings)
    sampled_data_attribute_loadings_sorted = sampled_data_attribute_loadings.copy()
    sampled_data_attribute_loadings_sorted.sort(reverse = True)
    print("sampled_data_attribute_loadings_sorted: ", sampled_data_attribute_loadings_sorted)
    top3_attributes_i_sampled_data = []
    for i in range(3):
        top3_attributes_i_sampled_data.append(sampled_data_attribute_loadings.index(sampled_data_attribute_loadings_sorted[i]))
    print()
    print("top3_attributes_i_sampled_data: ", top3_attributes_i_sampled_data)
    print("top 3 attributes with highest PCA loadings for sampled data:")
    for i in range(3):
        print("    ", df_sampled_data.columns[top3_attributes_i_sampled_data[i]])
    # ====== Compute the three attributes with highest PCA loadings -- end ======


    # ===============================================
    # Wrap data into a single json file for frontend to visualize
    # chart_data = df_all_data.to_dict()
    # chart_data = json.dumps(chart_data, indent=4)
    vis_data = {'pca_all_data_explained_variance_ratio_': pca_all_data_explained_variance_ratio_ls,
                'pca_sampled_data_explained_variance_ratio_': pca_sampled_data_explained_variance_ratio_ls}

    # vis_data = jsonify(vis_data) # Should be a json string
    return render_template("index.html", data=vis_data)


# =================== random sampling -- start ====================
def random_sampling(df_all_data):
    total_n_sample = int(len(df_all_data) / 2) # sample half of the data
    df_sampled_data = df_all_data.sample(n=total_n_sample)
    print("df_sampled_data:")
    print(df_sampled_data)
    print("Number of instance in df_sampled_data: %d" % len(df_sampled_data))
    print("Number of dimension of df_sampled_data: %d" % len(df_sampled_data.columns))
    df_sampled_data.columns = ['Apps','Accept','Enroll', 'Top10perc', 'Top25perc', 'F.Undergrad', 'P.Undergrad', 'Outstate',
    	       'Room.Board', 'Books', 'Personal', 'PhD', 'Terminal', 'S.F.Ratio', 'perc.alumni', 'Expend', 'Grad.Rate']
    return df_sampled_data
# =================== random sampling -- end =====================

# ================= stratified sampling -- start ==================
def stratified_sampling(df_all_data):
    # optimize k using elbow
    distortions = []
    n_k = range(1,10)
    decs = []
    pre_distortion = 0
    print("KMeans optimizing k using elbow")
    for k in n_k:
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(df_all_data)

        # using standard euclidean distance
        distortion = np.sum(np.min(cdist(df_all_data, kmeans.cluster_centers_, 'euclidean'), axis=1)) \
                            / df_all_data.shape[0]
        distortions.append(distortion)
        if k == 1: dec = -float("inf")
        else: dec = distortion - pre_distortion
        decs.append(dec)
        pre_distortion = distortion
        print("k: %d, distortion: %.4f, dec: %0.4f" % (k, distortion, dec))

    elbow_k = 0
    for i in range(2, len(decs) + 1):
        diff = decs[i + 1] - decs[i]
        if diff < 60:
            elbow_k = i
            break
    print("elbow_k: %d" % elbow_k)

    kmeans = KMeans(n_clusters=elbow_k)
    kmeans.fit(df_all_data)
    labels = kmeans.labels_
    # print(labels)

    # Append cluster_id column to df_all_data
    df_clusters = pd.DataFrame({'cluster_id': labels})
    df_all_data_with_clusters = df_all_data.join(df_clusters)
    # print(df_all_data_with_clusters)

    cluster_ratio = []
    labels_ls = labels.tolist()
    for i in range(elbow_k):
        cluster_ratio.append(float(labels_ls.count(i)) / float(len(labels)))
    print("cluster_ratio: ", cluster_ratio)

    # stratified sampling
    df_ss_data_ls = []
    total_n_sample = int(len(df_all_data) / 2) # sample half of the data
    for i in range(elbow_k):
        df_cluster_data = df_all_data_with_clusters.loc[df_all_data_with_clusters['cluster_id'] == i] # select rows whose cluster_id is i
        n_sample_cluster_i = int(total_n_sample * cluster_ratio[i]) # sample number in cluster i is based on the corresponding ratio
        df_sampled_cluster_data = df_cluster_data.sample(n=n_sample_cluster_i)
        df_ss_data_ls.append(df_sampled_cluster_data)

    df_ss_data = pd.DataFrame() # stratified sampled data
    print("Population of df_all_data: %d" % len(df_all_data))
    for i in range(elbow_k):
        df_ss_data = df_ss_data.append(df_ss_data_ls[i])
        print("Number of cluster %d: %d" % (i, len(df_ss_data_ls[i])))
    print("Number of instance in df_ss_data: %d" % len(df_ss_data))
    print("Number of dimension of df_ss_data: %d" % len(df_ss_data.columns))
    df_ss_data.columns = ['Apps','Accept','Enroll', 'Top10perc', 'Top25perc', 'F.Undergrad', 'P.Undergrad', 'Outstate',
    	       'Room.Board', 'Books', 'Personal', 'PhD', 'Terminal', 'S.F.Ratio', 'perc.alumni', 'Expend', 'Grad.Rate', 'Cluster']
    return df_ss_data
# ================= stratified sampling -- end ==================




if __name__ == "__main__":
    df = pd.read_csv('College.csv')
    app.run(debug=True)
