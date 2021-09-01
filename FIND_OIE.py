#STEP 3 - FIND OIE AND EOIE - JULY/2021

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib

main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/" 

#choose accordingly: sec vs min analysis
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRN/"
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNmin/"

figs_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/figs/"


ghi =  ['GHIP_SI02pt100',
        'GHIP_SMP11',
        'GHIP_SMP22',
        'GHIP_SPN1',
        'GHIT_SMP22']

kt =  ['kt_GHIP_SI02pt100',
       'kt_GHIP_SMP11',
       'kt_GHIP_SMP22',
       'kt_GHIP_SPN1',
       'kt_GHIT_SMP22']

gti = ['TGHIP_SI02pt100', 
       'TGHIP_SI02pt100_dirty',
       'TGIP_SMP11_VENT']
      
fghi = ['F_GHIP_SI02pt100', 
        'F_GHIP_SMP11', 
        'F_GHIP_SMP22', 
        'F_GHIP_SPN1', 
        'F_GHIT_SMP22']


dif = ['DfHIP_SPN1', 
       'DfHIRP_SMP11',
       'DfHIT_SMP22',
       'DIF_GLO_REF_SPN1']

dni = ['DNI_SHP1']

months = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
          '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
          '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
          '2021-01']

years = ['2018', '2019', '2020', '2021']

dfghi = pd.DataFrame(columns = ghi)

solar_constant = 1366.1

ghibins = [1300,1350,1400,1450,1500,1550,1600,1650,1700,1750,1800,1850,1900,1950,2000]

# RETRIEVE

## CRITERIA 1: GHI/ETH =  KT > 1 ############


for year in years: 
       print(year)
       dfghi = pd.read_pickle(BSRN_path + year +'ghiFLAG.pkl')
       #dfghi['sumflags']= dfghi.iloc[:,4:8].sum(axis=1)
       eth   = pd.read_pickle(BSRN_path + year + 'ETH.pkl')
       eth.rename(columns= {0: "eth"}, inplace=True)
       dfghi[kt] = dfghi[ghi]
       dfghi[kt] = dfghi[kt].div(eth.eth.values, axis=0)
       
       GHIP_SI02 = pd.DataFrame(columns = ['ghi', 'flag', 'kt','delta', 'isstart', 'isend'])
       GHIP_SI02['ghi']  = dfghi['GHIP_SI02pt100']
       GHIP_SI02['flag'] = dfghi['F_GHIP_SI02pt100']
       GHIP_SI02['kt']   = dfghi['kt_GHIP_SI02pt100']
       GHIP_SI02   = GHIP_SI02[GHIP_SI02.flag < 4]

       GHIP_SMP11 = pd.DataFrame(columns = ['ghi', 'flag', 'kt','delta', 'isstart', 'isend'])
       GHIP_SMP11['ghi']  = dfghi['GHIP_SMP11']
       GHIP_SMP11['flag'] = dfghi['F_GHIP_SMP11']
       GHIP_SMP11['kt']   = dfghi['kt_GHIP_SMP11']
       GHIP_SMP11 = GHIP_SMP11[GHIP_SMP11.flag < 4]

       GHIP_SMP22 = pd.DataFrame(columns = ['ghi', 'flag', 'kt','delta', 'isstart', 'isend'])
       GHIP_SMP22['ghi']  = dfghi['GHIP_SMP22']
       GHIP_SMP22['flag'] = dfghi['F_GHIP_SMP22']
       GHIP_SMP22['kt']   = dfghi['kt_GHIP_SMP22']
       GHIP_SMP22 = GHIP_SMP22[GHIP_SMP22.flag < 4]

       GHIT_SMP22 = pd.DataFrame(columns = ['ghi', 'flag', 'kt','delta', 'isstart', 'isend'])
       GHIT_SMP22['ghi']  = dfghi['GHIT_SMP22']
       GHIT_SMP22['flag'] = dfghi['F_GHIT_SMP22']
       GHIT_SMP22['kt']   = dfghi['kt_GHIT_SMP22']
       GHIT_SMP22 = GHIT_SMP22[GHIT_SMP22.flag <4]

       GHIP_SPN1 = pd.DataFrame(columns = ['ghi', 'flag', 'kt', 'delta', 'isstart', 'isend'])
       GHIP_SPN1['ghi']  = dfghi['GHIP_SPN1']
       GHIP_SPN1['flag'] = dfghi['F_GHIP_SPN1']
       GHIP_SPN1['kt']   = dfghi['kt_GHIP_SPN1']
       GHIP_SPN1 = GHIP_SPN1[GHIP_SPN1.flag <4]

          
       oie_GHIP_SI02  = GHIP_SI02[GHIP_SI02['kt']>1]   
       oie_GHIP_SMP11 = GHIP_SMP11[GHIP_SMP11['kt']>1]   
       oie_GHIP_SMP22 = GHIP_SMP22[GHIP_SMP22['kt']>1]   
       oie_GHIT_SMP22 = GHIT_SMP22[GHIT_SMP22['kt']>1]   
       oie_GHIP_SPN1  = GHIP_SPN1[GHIP_SPN1['kt']>1]   

       print(oie_GHIP_SI02.describe())
       ghihist = oie_GHIP_SI02.ghi.hist()
       gfigname = figs_path + 'GHIOIEminSI02' + year +'.jpeg'
       fig = ghihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       khist  = oie_GHIP_SI02.kt.hist()
       kfigname = figs_path + 'KtOIEminSI02' + year +'.jpeg'
       fig = khist.get_figure()
       fig.savefig(kfigname)
       fig.clf()

       print(oie_GHIP_SMP11.describe())
       ghihist = oie_GHIP_SMP11.ghi.hist()
       gfigname = figs_path + 'GHIOIEminSMP11' + year +'.jpeg'
       fig = ghihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       khist  = oie_GHIP_SMP11.kt.hist()
       kfigname = figs_path + 'KtOIEminSMP11' + year +'.jpeg'
       fig = khist.get_figure()
       fig.savefig(kfigname)
       fig.clf()

       print(oie_GHIP_SMP22.describe())
       ghihist = oie_GHIP_SMP22.ghi.hist()
       gfigname = figs_path + 'GHIOIEminSMP22' + year +'.jpeg'
       fig = ghihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       khist  = oie_GHIP_SMP22.kt.hist()
       kfigname = figs_path + 'KtOIEminSMP22' + year +'.jpeg'
       fig = khist.get_figure()
       fig.savefig(kfigname)
       fig.clf()

       print(oie_GHIT_SMP22.describe())
       ghihist = oie_GHIT_SMP22.ghi.hist()
       gfigname = figs_path + 'GHIOIEminTSMP22' + year +'.jpeg'
       fig = ghihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       khist  = oie_GHIT_SMP22.kt.hist()
       kfigname = figs_path + 'KtOIEminTSMP22' + year +'.jpeg'
       fig = khist.get_figure()
       fig.savefig(kfigname)
       fig.clf()

       print(oie_GHIP_SPN1.describe())
       ghihist = oie_GHIP_SPN1.ghi.hist()
       gfigname = figs_path + 'GHIOIEminSPN1' + year +'.jpeg'
       fig = ghihist.get_figure()
       fig.savefig(gfigname)
       fig.clf()
       khist  = oie_GHIP_SPN1.kt.hist()
       kfigname = figs_path + 'KtOIEminSPN1' + year +'.jpeg'
       fig = khist.get_figure()
       fig.savefig(kfigname)
       fig.clf()


       oie_GHIP_SI02.loc[:,'delta'] = oie_GHIP_SI02.index.to_series().diff()/np.timedelta64(1,"m")  #FOR SECONDS MUST CHANGE HERE
       oie_GHIP_SI02.iloc[0,3] = 1.1
       oie_GHIP_SI02.loc[:,'isstart'] = (oie_GHIP_SI02.delta > 1 )
       oie_GHIP_SI02.loc[:,'isend'] = oie_GHIP_SI02.isstart.shift(-1)
       oie_GHIP_SI02.iloc[-1,5] = True

       oie_GHIP_SMP11.loc[:,'delta'] = oie_GHIP_SMP11.index.to_series().diff()/np.timedelta64(1,"m") #FOR SECONDS MUST CHANGE HERE
       oie_GHIP_SMP11.iloc[0,3]= 1.1
       oie_GHIP_SMP11.loc[:,'isstart'] = (oie_GHIP_SMP11.delta > 1 )
       oie_GHIP_SMP11.loc[:,'isend'] = oie_GHIP_SMP11.isstart.shift(-1)
       oie_GHIP_SMP11.iloc[-1,5] = True

       oie_GHIP_SMP22.loc[:,'delta'] = oie_GHIP_SMP22.index.to_series().diff()/np.timedelta64(1,"m") #FOR SECONDS MUST CHANGE HERE
       oie_GHIP_SMP22.iloc[0,3] = 1.1
       oie_GHIP_SMP22.loc[:,'isstart'] = (oie_GHIP_SMP22.delta > 1 )
       oie_GHIP_SMP22.loc[:,'isend'] = oie_GHIP_SMP22.isstart.shift(-1)
       oie_GHIP_SMP22.iloc[-1,5] = True

       oie_GHIT_SMP22.loc[:,'delta'] = oie_GHIT_SMP22.index.to_series().diff()/np.timedelta64(1,"m") #FOR SECONDS MUST CHANGE HERE
       oie_GHIT_SMP22.iloc[0,3] = 1.1
       oie_GHIT_SMP22.loc[:,'isstart'] = (oie_GHIT_SMP22.delta > 1 )
       oie_GHIT_SMP22.loc[:,'isend'] = oie_GHIT_SMP22.isstart.shift(-1)
       oie_GHIT_SMP22.iloc[-1,5] = True

       oie_GHIP_SPN1.loc[:,'delta'] = oie_GHIP_SPN1.index.to_series().diff()/np.timedelta64(1,"m") #FOR SECONDS MUST CHANGE HERE
       oie_GHIP_SPN1.iloc[0,3] = 1.1
       oie_GHIP_SPN1.loc[:,'isstart'] = (oie_GHIP_SPN1.delta > 1 )
       oie_GHIP_SPN1.loc[:,'isend'] = oie_GHIP_SPN1.isstart.shift(-1)
       oie_GHIP_SPN1.iloc[-1,5] = True

       # Table with all OIE - Criteria 1
       
       eventsC1SI02 = pd.DataFrame(columns = ['start', 'end', 'duration', 'ibe', 'min', 'max', 'average'])
       eventsC1SI02['start']    = oie_GHIP_SI02.loc[oie_GHIP_SI02.start == True].index
       eventsC1SI02['end']      = oie_GHIP_SI02.loc[oie_GHIP_SI02.end == True].index
       eventsC1SI02['duration'] = events.end  - events.start
       eventsC1SI02['ibe']      = events.start - events.start.shift(+1)
       df1 = eventsC1SI02min.loc[:,'start': 'end']
       df2 = pd.DataFrame(columns = ['ghi'])
       df2['ghi']  = oie_GHIP_SI02['ghi']
       df1['list'] = df1.apply(lambda x : pd.date_range(start =x['start'],end=x['end'],freq='min').tolist(),axis=1)  ###  FOR SECONDS MUST CHANGE HERE
       df1 = df1['list'].apply(pd.Series).stack().to_frame().rename(columns={0:'Date'})
       df1['value'] = df1.Date.map(df2.rates)
       avg = df1.groupby(level=0).mean()
       min = df1.groupby(level=0).min()
       max = df1.groupby(level=0).max()
       eventsC1SI02['avg'] = avg['value']
       eventsC1SI02['min'] = avg['min']
       eventsC1SI02['max'] = avg['max']
       df1 = []
       df2 = []
       
       
       
       
       
       
       eventsC1SPN1 = pd.DataFrame(columns = ['start', 'end', 'duration', 'ibe', 'min', 'max', 'average'])
       eventsC1SPN1['start']    = oie_GHIP_SPN1.loc[oie_GHIP_SPN1.start == True].index
       eventsC1SPN1['end']      = oie_GHIP_SPN1.loc[oie_GHIP_SPN1.end == True].index
       eventsC1SPN1['duration'] = events.end  - events.start
       eventsC1SPN1['ibe']      = events.start - events.start.shift(+1)
     
       df1 = eventsC1SPN1min.loc[:,'start': 'end']
       df2 = pd.DataFrame(columns = ['ghi'])
       df2['ghi']  = oie_GHIP_SPN1['ghi']
       df1['list'] = df1.apply(lambda x : pd.date_range(start =x['start'],end=x['end'],freq='min').tolist(),axis=1)  ###  FOR SECONDS MUST CHANGE HERE
       df1 = df1['list'].apply(pd.Series).stack().to_frame().rename(columns={0:'Date'})
       df1['value'] = df1.Date.map(df2.rates)
       avg = df1.groupby(level=0).mean()
       min = df1.groupby(level=0).min()
       max = df1.groupby(level=0).max()
       
       eventsC1SPN1['avg'] = avg['value']
       eventsC1SPN1['min'] = avg['min']
       eventsC1SPN1['max'] = avg['max']
       df1 = []
       df2 = []






       # EXTRACT: max intensity  - duration - average intensity - interval between events - FOR ALL EVENTS

## CRITERIA 2: GTI > G0 = 1366.1  (NREL)############

       oie_gti = dfgti[dfgti > solar_constant]

  dfgti = pd.read_pickle(main_path+year+'GTI.pkl')
       dfgti = dfgti.resample('1Min').mean()  # use in case of 1 min span

# EXTRACT: max intensity  - duration - average intensity - interval between events - FOR ALL EVENTS
