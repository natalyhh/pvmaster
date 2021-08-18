#  STEP 1 - CLEANDATA - JULY/2021 - 

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib   # v 0.7.2

##  1) IMPORT FILE AND SELECT ONLY USEFUL VARIABLES. DEFINE A WORKABLE TIME RECORD STANDARD.
##      a) Check if all files for the given year have he same entries.
##      b) Compile all files into one single time series.

main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/"

PATHS = ["/Users/nataly/opt/AnacondaProjects/SAPIENS/original/2018/CR3000/Sec/*.dat",
         "/Users/nataly/opt/AnacondaProjects/SAPIENS/original/2019/CR3000/Sec/*.dat",
         "/Users/nataly/opt/AnacondaProjects/SAPIENS/original/2020/CR3000/Sec/*.dat",
         "/Users/nataly/opt/AnacondaProjects/SAPIENS/original/2021/CR3000/Sec/*.dat"]

column_names = ['TIMESTAMP',
                'GHIP_SI02pt100',
                'GHIP_SMP11',
                'GHIP_SMP22',
                'GHIP_SPN1',
                'GHIT_SMP22',
                'TGHIP_SI02pt100', 
                'TGHIP_SI02pt100_dirty',
                'TGIP_SMP11_VENT',
                'DfHIP_SPN1', 
                'DfHIRP_SMP11',
                'DfHIT_SMP22',
                'DIF_GLO_REF_SPN1',
                'DNI_SHP1',
                'LW_SGR4', 
                'wind_speed', 
                'wind_direction']

ghi =  ['GHIP_SI02pt100',
        'GHIP_SMP11',
        'GHIP_SMP22',
        'GHIP_SPN1',
        'GHIT_SMP22']

gti = ['TGHIP_SI02pt100', 
       'TGHIP_SI02pt100_dirty',
       'TGIP_SMP11_VENT']
      
dif = ['DfHIP_SPN1', 
       'DfHIRP_SMP11',
       'DfHIT_SMP22',
       'DIF_GLO_REF_SPN1']

dni = ['DNI_SHP1']
  
wind = ['wind_speed', 
        'wind_direction']
                
compdata = pd.DataFrame(columns = column_names)

#file_duration = pd.DataFrame(index = datafiles , columns = ['Tstart','Tend', 'Istart','Iend'])

months = ['2018-01','2018-02','2018-03', '2018-04','2018-05','2018-06','2018-07','2018-08', '2018-09','2018-10','2018-11','2018-12',
          '2019-01','2019-02','2019-03', '2019-04','2019-05','2019-06','2019-07','2019-08', '2019-09','2019-10','2019-11','2019-12',
          '2020-01','2020-02','2020-03', '2020-04','2020-05','2020-06','2020-07','2020-08', '2020-09','2020-10','2020-11','2020-12',
          '2021-01']

years = ['2018','2019','2020','2021']


#END DEFINITIONS

##############################################################################
## cleandata

for path in PATHS:
    datafiles = glob.glob(path)
    datafiles.sort()
    for file in datafiles:
        df = pd.read_csv(file, usecols=column_names)[column_names]        

        df[['GHIP_SI02pt100','GHIP_SMP11','GHIP_SMP22','GHIP_SPN1','GHIT_SMP22',
            'TGHIP_SI02pt100','TGHIP_SI02pt100_dirty','TGIP_SMP11_VENT',
            'DfHIP_SPN1','DfHIRP_SMP11','DfHIT_SMP22','DIF_GLO_REF_SPN1',
            'DNI_SHP1','LW_SGR4', 'wind_speed','wind_direction']] = df[['GHIP_SI02pt100',
            'GHIP_SMP11','GHIP_SMP22','GHIP_SPN1','GHIT_SMP22','TGHIP_SI02pt100',
            'TGHIP_SI02pt100_dirty','TGIP_SMP11_VENT','DfHIP_SPN1','DfHIRP_SMP11',
            'DfHIT_SMP22','DIF_GLO_REF_SPN1','DNI_SHP1','LW_SGR4', 'wind_speed',
            'wind_direction']].astype("float64")  
        df['TIMESTAMP'] = df['TIMESTAMP'].astype(np.datetime64)
                 
        df = df.fillna(-9999)
        df = df.sort_values(by=['TIMESTAMP'])
        df= df.drop_duplicates()
        compdata = pd.concat([compdata, df])
        # PARA CADA ARQUIVO CHECAR: TIMESTAMP INICIO / FIM
        #file_duration.at[path,'Tstart']= df.iloc[0,0]
        #file_duration.at[path,'Tend'  ]= df.iloc[-1,0]    
        #file_duration.at[path,'Istart']= df.index[0]
        #file_duration.at[path,'Iend'  ]= df.index[-1]  

print(compdata.shape)
compdata = compdata.sort_values(by=['TIMESTAMP'])
compdata = compdata.drop_duplicates() # CAREFUL - NEED TO CHECK - DROPS ONLY WHEN ALL ENTRIES ARE IDENTICAL. HOWEVER, AFTER SUBSETTING DUPLICATES ARE STILL FOUND.
compdata = compdata.reset_index(drop=True)
print(compdata.shape)

dataserie = compdata.set_index('TIMESTAMP')

dataserie.to_pickle(main_path+'FULLdata.pkl')


# STILL NEED TO CHECK WEIRD DATA BEHAVIOR. REGARDING DUPLICATE VALUE MISMATCHS

#############################################################################
# PLOTS - VISUAL CHECK

ghidata  = dataserie[ghi]  
gtidata  = dataserie[gti]  
difdata  = dataserie[dif]  
dnidata  = dataserie[dni]
winddata = dataserie[wind] 


for month in months:
    ghiplot = ghidata.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'GHI '+ month+'.jpeg'
    fig = ghiplot[0].get_figure()
    fig.savefig(figname)
    
    gtiplot = gtidata.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'GTI '+ month+'.jpeg'
    fig = gtiplot[0].get_figure()
    fig.savefig(figname)

    difplot = difdata.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'DIF '+ month+'.jpeg'
    fig = difplot[0].get_figure()
    fig.savefig(figname)

    dniplot = dnidata.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'DNI '+ month+'.jpeg'
    fig = dniplot[0].get_figure()
    fig.savefig(figname)
    
    #windplot = winddata.loc[month].plot(subplots=True, figsize=(20,30)) - RETHINK SCALES
    #figname = 'Wind '+ month+'.jpeg'
    #fig = windplot[0].get_figure()
    #fig.savefig(figname)


# SAVE CLEAN DATA BY YEAR:
for year in years:
    dfghi = ghidata.loc[year]
    dfgti = gtidata.loc[year]
    dfdif = difdata.loc[year]
    dfdni = dnidata.loc[year]
    dfwind = winddata.loc[year]

    dfghi.to_pickle(main_path+year+'GHI.pkl')
    dfgti.to_pickle(main_path+year+'GTI.pkl')
    dfdif.to_pickle(main_path+year+'DIF.pkl')
    dfdni.to_pickle(main_path+year+'DNI.pkl')


#############################################################################
'''BSRN TEST  - GIULIANO MARTINS - Evaluating the performance of radiometers for solar overirradiance events - PRE PRINT SOLAR ENERGY


### latitude, longitude, name, altitude, timezone - data retrieved in local time.
location = pvlib.location.Location(-27.430891, -48.441406, tz = 'ETC/GMT',altitude= 2.74, name = 'Florianopolis')  ## check for daylight savings 'Etc/GMT-3' 'America/Sao_Paulo'
naive_times = pd.date_range(start = compdata['TIMESTAMP'].min(), end = compdata['TIMESTAMP'].max(), freq='1s', tz = location.tz)
naive_times = pd.DatetimeIndex(naive_times)

eth = pvlib.irradiance.get_extra_radiation(naive_times, solar_constant = 1366.1, method = 'nrel').to_frame()
solpos = pvlib.solarposition.get_solarposition(naive_times, location.latitude, location.longitude, location.altitude, pressure = 101293, temperature = 25)

cosSZA = np.cos(np.deg2rad(solpos.azimuth))
PPmin = -4
ERmin = -2

ghiPP['max'] = eth[0]*1.5*cosSZA[0]**(1.2) + 100
ghiPP['min'] = PPmin

difPP['max'] = eth[0]*0.95*cosSZA[0]**(1.2) + 50
difPP['min'] = PPmin

dniPP['max'] = eth[0]
dniPP['min'] = eth[0]

ghiER['max'] = eth[0]*1.2*cosSZA[0]**(1.2) + 50
ghiER['min'] = ERmin

difER['max'] = eth[0]*0.75*cosSZA[0]**(1.2)+ 30
difER['min'] = ERmin

dniER['max'] = eth[0]*0.95*cosSZA[0]**(0.2)+10
dniER['min'] = ERmin



### GOALS 10/07/21 ###
# 1) SAVE CLEAR DATA PER YEAR
#
# 2) BSRN - finish codng with sample:
#    A) COMPARE DATA
#    B) FLAG
#    C) SAVE
#
# 3) FIND OIE and EOIE per year
# 
# 4) DC CURRENT BEHAVIOR
# 
# 5) FIRST VERSION OF THE TEXT. 



# now how to implement the cross comparisons?
# BSRN QUALITY CHECKS
#
# PHYSICALLY POSSIBLE LIMITS - L1 - PP
#
# GHI
# Min : -4 Wm^{-2} 
# Max : Sa x 1.5 x cos(SZA)^{1.2} + 100 Wm^{-2}
#
# DIF
# Min : -4 Wm^{-2}
# Max : Sa x 0.95 x cos(SZA)^{1.2} + 50 Wm^{-2}
#
# DNI
# Min : -4 Wm^{-2}
# Max : Sa 
#
#
# EXTREMELY RARE LIMITS - L2 - ER
#
# GHI
# Min : -2 Wm^{-2}
# Max : Sa x 1.2 x cos(SZA)^{1.2} + 50 Wm^{-2}
#
# DIF
# Min : -2 Wm^{-2}
# Max : Sa x 0.75 x cos(SZA)^{1.2} + 30 Wm^{-2}
#
# DNI
# Min : -2 Wm^{-2}
# Max : Sa x 0.95 x cos(SZA)ˆ{0.2} + 10 Wm^{-2}
#
# COMPARISONS - NON-DEFINITVE  L3 - CT
#  many devices. which ones will be chosen?
#
# GHI
# SumSZA = DIF + (DNI x cos(SZA) - 
# for SumSZA > 50Wm^{-2}:
#  if SZA < 75 deg 
#      0.92 < GHI/[DIF + (DNI x cos(SZA))] < 1.08
#  if 93 deg > SZA > 75 deg 
#      0.85 < GHI/[DIF + (DNI x cos(SZA))] < 1.15
# for SumSZA < 50Wm^{-2}:
#   N.A
# 
# DIF 
# for GHI > 50Wm^{-2}:
#  if SZA < 75 deg 
#      GHI/DIF  < 1.05
#  if 93 deg > SZA > 75 deg 
#      GHI/DIF < 1.10
# for GHI < 50Wm^{-2}:
#   N.A
#
# FLAGS:
# -1 - missing data or test not possible
#  0 - No test failures
#  1 - too low  (CT) 
#  2 - too high (CT) 
#  3 - too low  (ER) 
#  4 - too high (ER) 
#  5 - too low  (PP) 
#  6 - too high (PP)
#
# REJECTED FLAGS: SET VALUE TO -999
# POSSIBLY AID ANALYSIS WITH PLOTS
'''