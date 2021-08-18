#STEP 3.3 - FIND  EOIE with FLAG GTI - per minute - JULY/2021

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib  # v 0.7.2

main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/" 

#choose accordingly: sec vs min analysis
#BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRN/"
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNminGTI/"

figs_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/figs/"



sensors =  ['TGHIP_SI02pt100', 
             'TGHIP_SI02pt100_dirty',
             'TGIP_SMP11_VENT']


solar_constant = 1366.1


#months = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
#          '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
#          '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
#          '2021-01']

years = ['2018', '2019', '2020', '2021']

dfgti = pd.DataFrame(columns = sensors)

#gtibins = [1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]




####### CRITERIA 2: GTI  > SC ############


for year in years: 
    print(year)
    dfgti = pd.read_pickle(BSRN_path + year +'gtiFLAG.pkl')
    #eth   = pd.read_pickle(BSRN_path + year + 'ETH.pkl')
    #eth.rename(columns= {0: "eth"}, inplace=True)
    #dfgti[kt] = dfgti[sensors]
    #dfgti[kt] = dfgti[kt].div(eth.eth.values, axis=0)

    for sensor in sensors:
       print(sensor)
       dfGTI = pd.DataFrame(columns = ['gti', 'flag','delta', 'isstart', 'isend'])
       oie = pd.DataFrame(columns = ['gti', 'flag','delta', 'isstart', 'isend'])

       dfGTI['gti']  = dfgti[sensor]
       dfGTI['flag'] = dfgti['F_'+ sensor]
       dfGTI   = dfGTI[dfGTI.flag < 4]

       oie  = dfGTI[dfGTI['gti'] > solar_constant]   
       
       dfstat = oie.describe()
       dfstat.to_csv(BSRN_path + year + sensor + '_statsmin.csv')

       print(dfstat)
       gtihist = oie.gti.hist()
       gfigname = figs_path + year + 'gti_OIEmin_'+ sensor +'.jpeg'
       fig = gtihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       
       
       oie.loc[:,'delta'] = oie.index.to_series().diff()/np.timedelta64(1,"m")  #FOR SECONDS MUST CHANGE HERE
       oie.iloc[0,2] = 1.1
       oie.loc[:,'isstart'] = (oie.delta > 1 )
       oie.loc[:,'isend'] = oie.isstart.shift(-1)
       oie.iloc[-1,4] = True

       
       # Table with all OIEE - Criteria 2
       
       eventsC2 = pd.DataFrame(columns = ['start', 'end', 'duration', 'ibe', 'min', 'max', 'avg'])     ### WILL NEED KT  TOO IN THIS SUMMARY!!!
       eventsC2['start']    = oie.loc[oie.isstart == True].index
       eventsC2['end']      = oie.loc[oie.isend == True].index
       eventsC2['duration'] = eventsC2.end  - eventsC2.start
       eventsC2['ibe']      = eventsC2.start - eventsC2.start.shift(+1)
       df1 = eventsC2.loc[:,'start': 'end']
       df2 = pd.DataFrame(columns = ['gti'])
       df2['gti']  = oie['gti']
       df1['list'] = df1.apply(lambda x : pd.date_range(start =x['start'],end=x['end'],freq='min').tolist(),axis=1)  ###  FOR SECONDS MUST CHANGE HERE
       df1 = df1['list'].apply(pd.Series).stack().to_frame().rename(columns={0:'Date'})
       df1['value'] = df1.Date.map(df2.gti)
       avg = df1.groupby(level=0).mean()
       min = df1.groupby(level=0).min()
       max = df1.groupby(level=0).max()
       eventsC2['avg'] = avg['value']
       eventsC2['min'] = min['value']
       eventsC2['max'] = max['value']
       eventsC2.to_csv(BSRN_path + year + sensor + '_OIEC2min.csv')

       eventsC2 = {}
       df1 = {}
       df2 = {} 
       
  




# EXTRACT: max intensity  - duration - average intensity - interval between events - FOR ALL EVENTS

## CRITERIA 2: GTI > G0 = 1366.1  (NREL)############

    #   oie_gti = dfgti[dfgti > solar_constant]
    #dfgti = pd.read_pickle(main_path+year+'GTI.pkl')
    #   dfgti = dfgti.resample('1Min').mean()  # use in case of 1 min span

# EXTRACT: max intensity  - duration - average intensity - interval between events - FOR ALL EVENTS