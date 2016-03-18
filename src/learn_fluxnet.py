#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.cross_validation import ShuffleSplit

def main():

    fluxnet = pickle.load(open(DIRPATH + FILEPATH, 'rb'))

    #{'target': fluxnet.ix[:, :6], 'data': fluxnet.ix[:, 6:]}

    fnet_target = np.array(fluxnet.ix[:, 1:5])
    fnet_data = np.array(fluxnet.ix[:, 6:])

    # hold back 40% of the dataset for testing
    X_train, X_test, Y_train, Y_test = \
        cross_validation.train_test_split(fnet_data, fnet_target, \
                                          test_size=0.4, random_state=0)

# --------------------------------------------------------------------------------

    reg_model = GridSearchCV(DecisionTreeRegressor(max_depth=8), \
                             tuned_parameters, cv=5)

    regr_mod.fit(X_train, X_test)

# --------------------------------------------------------------------------------

    plt.plot(fluxnet['longitude'], fluxnet['latitude'], 'o')
    plt.show()


    return None

if __name__ == "__main__":

    DIRPATH = os.path.expanduser("~/Work/Research_Work/Drought_Workshop/PALS_site_datasets/flux/")
    FILEPATH = "fluxnet_data.pkl"

    main()
