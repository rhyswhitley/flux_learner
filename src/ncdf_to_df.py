#!/usr/bin/env python3

import os, re
import pickle
import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

from netCDF4 import Dataset
from datetime import datetime

# --------------------------------------------------------------------------------

def ncdf_2_df(nc_fname):

    # extract the site name from the basename of the filepath
    site_name = get_site_label(nc_fname)

    # open connection to netCDF file
    nc_con = Dataset(nc_fname, 'r')

    # extract all variable labels that have values
    headers = nc_con.variables.keys()

    # get timestream
    time_stamp = create_timestream(nc_con.variables['time'])

    # extract key and value pairs as a list of dicts
    dict_list = [get_value(nc_con, hd) for hd in headers] \
        + [site_name, time_stamp]

    # merge list into one dictionary
    one_dict = {key: val for dic in dict_list \
                for (key, val) in dic.items() \
                if key not in ['x', 'y', 'time']}

    # return a pandas dataframe to the user
    index_list = ['DT', 'site', 'elevation', 'latitude', 'longitude', 'reference_height']
    return pd.DataFrame(one_dict).set_index(index_list)

# --------------------------------------------------------------------------------

def get_site_label(filename):

    # extract the site name from the basename of the filepath
    site_lab = re.search('.+?(?=Fluxnet)', \
                         os.path.basename(filename)).group(0)

    # return a dict of the datetime stamps
    return {'site': site_lab}

# --------------------------------------------------------------------------------
def create_timestream(nc_var):

    # get date timestamp of origin
    str_origin = re.search('[0-9].*$', nc_var.units).group(0)
    # convert string to a datetime format
    dt_origin = datetime.strptime(str_origin, "%Y-%m-%d %H:%M:%S")

    # determine the timestep
    if dt_origin.minute is 0:
        tstep = 60
    else:
        tstep = dt_origin.minute

    # create a range of timestamp from the origin date for the length of
    # of the time-series at the specified frequency
    time_stamp = pd.date_range(dt_origin, freq="{0}min".format(tstep), \
                               periods=nc_var.shape[0])

    # return a dict of the datetime stamps
    return {'DT': time_stamp}

# --------------------------------------------------------------------------------

def get_value(nc_con, label):

    # extract values as a numpy array
    values = np.squeeze(nc_con.variables[label][:])

    # return a (key, value) dict
    return {label: values}

# --------------------------------------------------------------------------------

def quick_test(df_test, flux='NEE'):

    # testing stage here
    print(df_test.head(10))

    plt.figure(figsize=(10, 5))

    ax1 = plt.subplot(111)
    ax2 = ax1.twinx()

    ax1.plot_date(df_test.index, df_test[flux], 'r-', lw=1)
    ax2.plot_date(df_test.index, df_test[flux + '_qc'], '-', alpha=0.3)

    ax1.set_zorder(ax2.get_zorder() + 1)
    ax1.patch.set_visible(False)

    plt.show()

    return 1

# --------------------------------------------------------------------------------


def main():

    flux_fplist = [os.path.join(dp, f) for (dp, _, fn) in os.walk(DIRPATH) \
                   for f in fn if f.endswith("nc")]

    flux_dflist = [ncdf_2_df(fp) for fp in flux_fplist]

    pickle.dump(flux_dflist, open(DIRPATH + SAVEPATH, 'wb'), protocol=2)


if __name__ == "__main__":

    DIRPATH = os.path.expanduser("~/Work/Research_Work/Drought_Workshop/PALS_site_datasets/flux/")
    SAVEPATH = "fluxnet_raw_dataframes.pkl"

    main()



# old code


#def create_timestream(nc_var):
#
#    # get date timestamp of origin
#    str_origin = re.search('[0-9].*$', nc_var.units).group(0)
#    # convert string to a datetime format
#    dt_origin = datetime.strptime(str_origin, "%Y-%m-%d %H:%M:%S")
#
#    # convert the seconds since origin to a datetime stamp
#    t_labels = [dt_origin + timedelta(seconds=sec_i) \
#                for sec_i in nc_var[:]]
#
#    # return a dictionary of the datetime stamps
#    return {'DT': t_labels}

