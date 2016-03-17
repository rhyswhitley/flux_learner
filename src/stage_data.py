#!/usr/bin/env python3

import os, re
import pickle
import numpy as np
import pandas as pd

def clean_dataset(raw_df):

    # find the flag and data-value headers
    flag_hd = [cn for cn in raw_df.columns if "_qc" in cn]
    data_hd = [cn for cn in raw_df.columns if "_qc" not in cn]

    # split dataset up between values and flags
    flags = raw_df[flag_hd]
    datum = raw_df[data_hd]

    # mask the values dataframe using the flag dataframe
    data_masked = datum.mask(np.array(flags != 1), axis=0)

    # determine how much data is left to work with
    n_total = data_masked.shape[0]
    n_filt = data_masked.dropna(axis=0).shape[0]
    n_perc = n_filt/n_total * 100

    # echo to user
    print("Unfiltered data points are: ", n_total)
    print("Removing NaN -> reduced to: ", n_filt)
    print("Percentage of <reliable> data: {0:.2f} %".format(n_perc))

    return data_masked

def cast_dataset(new_df):

    # to cast will need to create new date and time columns
    new_df["Date"] = new_df.index.get_level_values('DT').date
    new_df["Time"] = new_df.index.get_level_values('DT').time

    # <there's got to be a better way to do this, but I'm essentially removing
    # the old DT index and replacing it with the Date stamp version>
    new_df.reset_index(['DT'], inplace=True)
    new_df.drop(['DT'], axis=1, inplace=True)
    new_df.set_index("Date", append=True, inplace=True)

    pivot_df = new_df.pivot(index=new_df.index, columns="Time")

    print(pivot_df.dropna(axis=0).shape[0])

    return 1

def stage_data(raw_df):

    clean_df = clean_dataset(raw_df)
    pivot_df = cast_dataset(clean_df)

    return 1

def main():

    flux_dflist = pickle.load(open(DIRPATH + "flux_dataframes.pkl", 'rb'))

    stage_data(flux_dflist[0])

    return 1

if __name__ == "__main__":

    DIRPATH = os.path.expanduser("~/Work/Research_Work/Drought_Workshop/PALS_site_datasets/flux/")

    main()
