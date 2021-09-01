## 1st JULY 2021
## BSRN ROUTINE FOR DATA QUALITY CHECK OF SOLAR IRRADIANCE DATA BEFORE OVERIRRADIANCE CHECK.
## reference: 
## (1)An Automated Quality Assessment and Control Algorithm for Surface Radiation Measurements - Long and Shi 2008
## (2)http://sonda.ccst.inpe.br/infos/validacao.html#criterios 
## (3)PV CAMPER article 
##
##  1) IMPORT FILE AND SELECT ONLY USEFUL VARIABLES. DEFINE A WORKABLE TIME RECORD STANDARD. 
##
##  2) DATA QUALITY CHECK PROCEDURE FOR GHI:
##      Level 1 tests: flag physically impossible values
##      Level 2 tests: flag extremely rare event
##      Level 3 tests: flag data inconsistent with same measurement from alternative sources of the station
##      Level 4 tests: flag data inconsistent with expected value from transposition model.  - TO BE DEFINED LATER
##
##      FLAGS: 
##
##  3) DATA QUALITY CHECK PROCEDURE FOR GTI:
##      
## 
##  4) SELECT ONLY DATA FLAGGED AS:   - HERE WILL HAVE TO DECIDE IF SPLIT DEVICES AND FOLLOW SEPARATELY OR NOT
##
##  5) FIND OVERIRRADIANCE EVENTS (OIE):
##      INPUT:
##      PRIMARY OUTPUT  : TIMESTAMP / MAX IRRADIANCE VALUE / DURATION / AVERAGE DURING EVENT /   
##      SECONDARY OUTPUT: ERROR ANALYSIS / INTERVAL BETWEEN TWO CONSECUTIVE OIE
##
##  6) FIND EXTREME OVERIRRADIANCE EVENTS (EOIE):
##      INPUT:
##      OUTPUT : TIMESTAMP / MAX IRRADIANCE VALUE / DURATION / AVERAGE DURING EVENT 
##      SECONDARY OUTPUT: ERROR ANALYSIS / INTERVAL BETWEEN TWO CONSECUTIVE EOIE / AVERAGE IRRADIANCE VALUE BEFORE EVENT (define meaningful interval duration)
##
##  7) COMPARE (5) AND (6) ACROSS ALL DEVICES AND ESTABLISH STATISTICS FOR THE DETECTED EVENTS. 
##      a) devices statistics
##      b) yearly statistics
##      c) plot: 
##          Histograms: max intensity, duration (EOI e OI) - OI will give more insight in the underlying processes. EOI will give more insight on PV damage.
##          Correlations: intensity vs duration, maximum intensity vs clearsky intensity (is there a typical intensity that triggers more this event, like a threshold?)
##
##  8) FOR PART 2, ONLY EOIE DETECTED IN ALL DEVICES WILL BE USED.
##
##
##   PART 2 - OPERATIONAL PERFORMANCE
##
##
##  9) IMPORT INVERTER FILES
##
##  10) QUALITY CHECK FOR NVERTER DATA (?)
##
##  11) CHOOSE MOST MEANINGFUL EOIE FROM PART 1. DEFINE A TIMESPAN, MAKING SURE TO INCLUDE BEFORE AND AFTER. EXTRACT INVERTER DATA FOR THAT INVERVAL.  
##
##  12) COMPARE DC / AC EOIE PERFORMANCE AGAINST DC / AC CLEARSKY PERFORMANCE IN SIMILAR DAY / TIME FOR EACH MODULE TECHNOLOGY.
##  
##  13) COMPARE DC / AC EOIE PERFORMANCE AGAINST FOR EACH MODULE TECHNOLOGY FOR DIFFERENT EVENTS DURATION (points of interest: highest, lowest and most frequent ones).
##
##  14) COMPARE DC OUTPUT WITH SIMULATED DC OUTPUT.
##
##  15) CALCULATE INVERTER OVERLOAD LOSSES FOR ALL THE EVENTS.
##  
##  16) more TBD.
##

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib
#from pvlib.location import Location
#from pvlib.solarposition import get_solarposition
#from pvlib import irradiance


##  1) IMPORT FILE AND SELECT ONLY USEFUL VARIABLES. DEFINE A WORKABLE TIME RECORD STANDARD.
##      a) Check if all files for the given year have he same entries.
##      b) Compile all files into one single time series.


# latitude, longitude, name, altitude, timezone - data retrieved in local time.
coordinates = [-27.430891, -48.441406, 'Florianopolis', 2.74, 'Brazil/East']  ## check for daylight savings 'Etc/GMT-3'

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

GHI =  ['GHIP_SI02pt100',
        'GHIP_SMP11',
        'GHIP_SMP22',
        'GHIP_SPN1',
        'GHIT_SMP22']

GTI = ['TGHIP_SI02pt100', 
       'TGHIP_SI02pt100_dirty',
       'TGIP_SMP11_VENT']
      
DIF = ['DfHIP_SPN1', 
       'DfHIRP_SMP11',
       'DfHIT_SMP22',
       'DIF_GLO_REF_SPN1']

DNI = ['DNI_SHP1']
  
WIND = ['wind_speed', 
        'wind_direction']
                
file_duration = pd.DataFrame(index = datafiles , columns = ['Tstart','Tend', 'Istart','Iend'])

compdata = pd.DataFrame(columns = column_names)

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
compdata = compdata.drop_duplicates()
compdata = compdata.reset_index(drop=True)
print(compdata.shape)


GHIdata = compdata['TIMESTAMP', GHI]  
GTIdata = compdata['TIMESTAMP', GTI]
    
# PLOTAR DIARIOS (POR MES? ANO? CADA VARIAVEL?)
#df.plot(subplots=True, figsize=(6, 6))

  


# DESCOBRIR O QUE ACONTECE NO HORARIO DE VERÃO:  
# 15/07/17 A 17/02/18 
# 04/11/18 A 16/02/19
 ## TIMESTAMP VS TIMEZONE  



'''





str1=r"C:\Users\Juca\Desktop\FV\EstacaoSolarimetrica\DADOS\TCC-Analise de Sensores\DadosComZenith\Min\*.dat"
interesting_files = glob.glob(str1) 




for path in interesting_files:
    df = pd.read_csv(path)
    df=df.fillna('-9999')
    df = df.convert_objects(convert_numeric=True)
    df['TIMESTAMP'] = df['TIMESTAMP'].astype(np.datetime64)
    ##Remeber to change the GMT according to datetime SITUATION
    tus = Location(-27.430891, -48.441406, 'Etc/GMT', 'Florianopolis')   ###(-27.430891, -48.441406, 'Etc/GMT', 'Florianopolis') ###Location(-12.31, -42.33, 'America/Bahia', 'BrotasdeMacauba')
    ##REMEMBER: Start and END according to what exists in the file
    times = pd.DatetimeIndex(start=df['TIMESTAMP'].min(), end=df['TIMESTAMP'].max(), freq='1min', tz=tus.tz)

    ext = irradiance.get_extra_radiation(times).to_frame()
    solpos = pvlib.solarposition.get_solarposition(times, tus.latitude, tus.longitude)
    ext['data'] = ext.index
    solpos['data'] = solpos.index

    extraterrestrial = ext.merge(solpos, left_on='data', right_on='data', how='inner')

    extraterrestrial['ext'] = extraterrestrial[0]
    extraterrestrial['ext'] = extraterrestrial['ext']*np.cos(extraterrestrial['zenith']*np.pi/180)
    extraterrestrial['max_fisico'] = 1.5*extraterrestrial[0]*(np.cos(extraterrestrial['zenith']*np.pi/180))**(1.2) + 100
    extraterrestrial['max_raro'] = 1.2*extraterrestrial[0]*(np.cos(extraterrestrial['zenith']*np.pi/180))**(1.2) + 50
    ext = extraterrestrial
    #ext = extraterrestrial.drop(['azimuth','elevation','equation_of_time', 'apparent_zenith', 'apparent_elevation','zenith', 0], axis=1)
    ext['max_fisico'].fillna(3000, inplace=True)
    ext['max_raro'].fillna(3000, inplace=True)

    ##Convert Columns to same dtype
    
    ext['data'] = ext['data'].astype(np.datetime64)
    ext = ext[['data','max_raro','max_fisico']]

    ##Merge Files according to their Timestamp
    df1 = df.merge(ext,left_on = 'TIMESTAMP' , right_on = 'data')
    ##Filter each value by BSRN parameter
    ##Filter GHIP_SMP22_Avg (1)
    df1.loc[df1['GHIP_SMP22_Avg'] > df1['max_fisico'] , 'FLAG_GHIP_SMP22'] = '2'
    df1.loc[df1['GHIP_SMP22_Avg'] < df1['max_raro'] , 'FLAG_GHIP_SMP22'] = '0'
    ##Filter GHIT_SMP22 (2)
    df1.loc[df1['GHIT_SMP22_Avg'] > df1['max_fisico'] , 'FLAG_GHIT_SMP22'] = '2'
    df1.loc[df1['GHIT_SMP22_Avg'] < df1['max_raro'] , 'FLAG_GHIT_SMP22'] = '0'
    ##Filter GHIP_SMP11 (3)
    df1.loc[df1['GHIP_SMP11_Avg'] > df1['max_fisico'] , 'FLAG_GHIP_SMP11'] = '2'
    df1.loc[df1['GHIP_SMP11_Avg'] < df1['max_raro'] , 'FLAG_GHIP_SMP11'] = '0'
    ##Filter GHIP_SPN1  (4)
    df1.loc[df1['GHIP_SPN1_Avg'] > df1['max_fisico'] , 'FLAG_GHIP_SPN1'] = '2'
    df1.loc[df1['GHIP_SPN1_Avg'] < df1['max_raro'] , 'FLAG_GHIP_SPN1'] = '0'
    ##Filter GHIP_SI02pt100 (5)
    df1.loc[df1['GHIP_SI02pt100_Avg'] > df1['max_fisico'] , 'FLAG_GHIP_SI02pt100'] = '2'
    df1.loc[df1['GHIP_SI02pt100_Avg'] < df1['max_raro'] , 'FLAG_GHIP_SI02pt100'] = '0'
    ##Filter GHIP_SR20  (6)
    df1.loc[df1['GHIP_SR20_Avg'] > df1['max_fisico'] , 'FLAG_GHIP_SR20'] = '2'
    df1.loc[df1['GHIP_SR20_Avg'] < df1['max_raro'] , 'FLAG_GHIP_SR20'] = '0'
    ##Filter GHIP_MS80  (7)
    df1.loc[df1['GHIP_MS80_Avg'] > df1['max_fisico'] , 'FLAG_GHIP_MS80'] = '2'
    df1.loc[df1['GHIP_MS80_Avg'] < df1['max_raro'] , 'FLAG_GHIP_MS80'] = '0'
    
    del df1['data']
    del df1['max_raro']
    del df1['max_fisico']
    df1[['FLAG_GHIP_SMP22','FLAG_GHIT_SMP22','FLAG_GHIP_SMP11','FLAG_GHIP_SPN1','FLAG_GHIP_SI02pt100','FLAG_GHIP_SR20','FLAG_GHIP_MS80']] = df1[['FLAG_GHIP_SMP22','FLAG_GHIT_SMP22','FLAG_GHIP_SMP11','FLAG_GHIP_SPN1','FLAG_GHIP_SI02pt100','FLAG_GHIP_SR20','FLAG_GHIP_MS80']].fillna('1')
    #OUTPUT CSV FILE
    df1.to_csv(path+'v4.dat',index=False)

'''