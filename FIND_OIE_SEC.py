#STEP 3.1 - FIND OIE AND EOIE - per second - JULY/2021
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
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRN/"
#BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNmin/"

figs_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/figs/"


#sensors =  ['GHIP_SI02pt100',
#            'GHIP_SMP11',
#            'GHIP_SMP22',
#            'GHIP_SPN1',
#            'GHIT_SMP22']
#kt =  ['kt_GHIP_SI02pt100',
#       'kt_GHIP_SMP11',
#       'kt_GHIP_SMP22',
#       'kt_GHIP_SPN1',
#       'kt_GHIT_SMP22']

sensors =  ['GHIP_SI02pt100',
            'GHIP_SMP11',
            'GHIP_SMP22',
            'GHIP_SPN1']


kt =  ['kt_GHIP_SI02pt100',
       'kt_GHIP_SMP11',
       'kt_GHIP_SMP22',
       'kt_GHIP_SPN1']

#gti = ['TGHIP_SI02pt100', 
#       'TGHIP_SI02pt100_dirty',
#       'TGIP_SMP11_VENT']
      
#fghi = ['F_GHIP_SI02pt100', 
#        'F_GHIP_SMP11', 
#        'F_GHIP_SMP22', 
#        'F_GHIP_SPN1', 
#        'F_GHIT_SMP22']


#dif = ['DfHIP_SPN1', 
#       'DfHIRP_SMP11',
#       'DfHIT_SMP22',
#       'DIF_GLO_REF_SPN1']

#dni = ['DNI_SHP1']

#months = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
#          '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
#          '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
#          '2021-01']

years = ['2018', '2019', '2020', '2021']

dfghi = pd.DataFrame(columns = sensors)

#solar_constant = 1366.1
#ghibins = [1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]




####### CRITERIA 1: GHI/ETH =  KT > 1 ############


for year in years: 
    print(year)
    dfghi = pd.read_pickle(BSRN_path + year +'ghiFLAG.pkl')
    eth   = pd.read_pickle(BSRN_path + year + 'ETH.pkl')
    eth.rename(columns= {0: "eth"}, inplace=True)
    dfghi[kt] = dfghi[sensors]
    dfghi[kt] = dfghi[kt].div(eth.eth.values, axis=0)

    for sensor in sensors:
       print(sensor)
       dfGHI = pd.DataFrame(columns = ['ghi', 'flag', 'kt','delta', 'isstart', 'isend'])
       oie = pd.DataFrame(columns = ['ghi', 'flag', 'kt','delta', 'isstart', 'isend'])

       dfGHI['ghi']  = dfghi[sensor]
       dfGHI['flag'] = dfghi['F_'+ sensor]
       dfGHI['kt']   = dfghi['kt_'+ sensor]
       dfGHI   = dfGHI[dfGHI.flag < 4]

       oie  = dfGHI[dfGHI['kt']>1]   
       
       dfstat = oie.describe()
       dfstat.to_csv(BSRN_path + year + sensor + '_statsC1sec.csv')

       print(dfstat)
       ghihist = oie.ghi.hist()
       gfigname = figs_path + year + 'GHI_OIEsec_'+ sensor +'.jpeg'
       fig = ghihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       khist  = oie.kt.hist()
       kfigname = figs_path + year + 'Kt_OIEsec_' + sensor + '.jpeg'
       fig = khist.get_figure()
       fig.savefig(kfigname)
       fig.clf()

       
       oie.loc[:,'delta'] = oie.index.to_series().diff()/np.timedelta64(1,"s")  #FOR SECONDS MUST CHANGE HERE
       oie.iloc[0,3] = 1.1
       oie.loc[:,'isstart'] = (oie.delta > 1 )
       oie.loc[:,'isend'] = oie.isstart.shift(-1)
       oie.iloc[-1,5] = True

       
       # Table with all OIE - Criteria 1
       
       eventsC1 = pd.DataFrame(columns = ['start', 'end', 'duration', 'ibe', 'min', 'max', 'avg'])   ### WILL NEED KT  TOO IN THIS SUMMARY!!!
       eventsC1['start']    = oie.loc[oie.isstart == True].index
       eventsC1['end']      = oie.loc[oie.isend == True].index
       eventsC1['duration'] = eventsC1.end  - eventsC1.start
       eventsC1['ibe']      = eventsC1.start - eventsC1.start.shift(+1)
       df1 = eventsC1.loc[:,'start': 'end']
       df2 = pd.DataFrame(columns = ['ghi'])
       df2['ghi']  = oie['ghi']
       df1['list'] = df1.apply(lambda x : pd.date_range(start =x['start'],end=x['end'],freq='sec').tolist(),axis=1)  ###  FOR SECONDS MUST CHANGE HERE
       df1 = df1['list'].apply(pd.Series).stack().to_frame().rename(columns={0:'Date'})
       df1['value'] = df1.Date.map(df2.ghi)
       avg = df1.groupby(level=0).mean()
       min = df1.groupby(level=0).min()
       max = df1.groupby(level=0).max()
       eventsC1['avg'] = avg['value']
       eventsC1['min'] = min['value']
       eventsC1['max'] = max['value']
       eventsC1.to_csv(BSRN_path + year + sensor + '_OIEC1sec.csv')

       eventsC1 = {}
       df1 = {}
       df2 = {}
       
       




# EXTRACT: max intensity  - duration - average intensity - interval between events - FOR ALL EVENTS

## CRITERIA 2: GTI > G0 = 1366.1  (NREL)############

    #   oie_gti = dfgti[dfgti > solar_constant]
    #dfgti = pd.read_pickle(main_path+year+'GTI.pkl')
    #   dfgti = dfgti.resample('1Min').mean()  # use in case of 1 min span

# EXTRACT: max intensity  - duration - average intensity - interval between events - FOR ALL EVENTS