#!/usr/bin/env python3

import os
import pickle
import numpy as np
import pandas as pd

def main():

    fluxnet = pickle.load(open(DIRPATH + FILEPATH, 'rb'))

    print(fluxnet.head())


    return None

if __name__ == "__main__":

    DIRPATH = os.path.expanduser("~/Work/Research_Work/Drought_Workshop/PALS_site_datasets/flux/")
    FILEPATH = "fluxnet_data.pkl"

    main()
