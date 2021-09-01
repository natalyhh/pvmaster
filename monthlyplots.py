#plots

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib

main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/" 
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRN/"



months18 = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12']

months19 = ['2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12']

months20 = ['2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12']

months21 = ['2021-01']


years = ['2018', '2019', '2020', '2021']




dfghi18 = pd.read_pickle(main_path+'2018GHI.pkl')
dfghi18 = dfghi18.resample('3Min').mean()  

for month in months18:
       df = dfghi['GHIP_SI02pt100']
       date = month +'-01'
       plt.figure()
       df.loc[date].plot()
       figname = 'GHI '+ date + '.jpeg'
       plt.savefig(figname)

       