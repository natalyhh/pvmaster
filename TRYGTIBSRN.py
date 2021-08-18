#STEP 2.3 - BSRN TEST ATTEMPT ON GTI - 1 MINUTE DATA - 

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib # v 0.7.2

# directory with clean and organized data per year for GHI, GTI, DIF, DNI
main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/" 

# directory to save BSRN test results
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNminGTI/" 


gti = ['TGHIP_SI02pt100', 
       'TGHIP_SI02pt100_dirty',
       'TGIP_SMP11_VENT']
      


fgti = ['F_TGHIP_SI02pt100', 
        'F_TGHIP_SI02pt100_dirty', 
        'F_TGIP_SMP11_VENT']

surface_tilt = 27

surface_azimuth = 0 # @south hemisphere facing north

months = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
          '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
          '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
          '2021-01']

years = ['2018', '2019', '2020', '2021']
#years = ['2019', '2020', '2021']
#years = ['2020', '2021']



#BSRN TEST

# latitude, longitude, name, altitude, timezone - data retrieved in ETC/GMT - as plotted = noon around 3 pm
location = pvlib.location.Location(-27.430891, -48.441406, tz = 'Etc/GMT', altitude= 2.74, name = 'Florianopolis')  # check for daylight savings 'Etc/GMT-3' 'Brazil/East' 'America/Sao_Paulo'

missing = pd.DataFrame(columns= ['days'], index = years) # count data record missing in a year, for each year. IN THE DATALOGGER. individual sensor may have empty entries not accounted for

#PPmin = -4  # minimum physically possible limit
#ERmin = -2  # minimum extremely rare limit

flags = [-1, #NaN
         -1, #-9999   - apparently did not appear?!?! TEST: create specific flag to track it.
          3, # too low PP
          4] # too high PP

gtiflagcount = pd.DataFrame(columns= [gti], index = [-1, 0, 3, 4], dtype = int) 


#### end definitions

for year in years:
    gtiFLAG = pd.DataFrame(columns = ['PPmax', 'PPmin', 
                                      'F_TGHIP_SI02pt100','F_TGHIP_SI02pt100_dirty', 
                                      'F_TGIP_SMP11_VENT'])
    
    dfgti = pd.read_pickle(main_path+year+'GTI.pkl')
    dfgti = dfgti.resample('1Min').mean()  
    print('dfgti.shape =', dfgti.shape,year)

    dfgti.index = dfgti.index.tz_localize(location.tz)
    
    naive_times = pd.date_range(start = dfgti.index.min(), end = dfgti.index.max(), freq='1Min', tz = location.tz)
    naive_times = pd.DatetimeIndex(naive_times)   # PROBLEM: WILL HAVE TO DEAL WITH MISSING VALUES
    print('NAIVE.shape =', naive_times.shape,year)

    missing.loc[year] = (len(naive_times) - len(dfgti.index))/3600/24

    eth = pvlib.irradiance.get_extra_radiation(naive_times, solar_constant = 1366.1, method = 'nrel').to_frame()
    solpos = pvlib.solarposition.get_solarposition(naive_times, location.latitude, location.longitude, location.altitude, pressure = 101293, temperature = 25)

    aoi = pvlib.irradiance.aoi(surface_tilt, surface_azimuth, solpos.zenith, solpos.azimuth)

    cosaoi = np.cos(np.deg2rad(aoi)).to_frame()
    cosSZA = np.cos(np.deg2rad(solpos.zenith)).to_frame()
   
    gtiFLAG['PPmax'] = eth[0]*(cosaoi.aoi + (cosSZA.zenith**(1.2))) + 150
    gtiFLAG['PPmin'] = (-4)*(cosaoi.aoi + 2)

    print('gtiFLAG.shape =', gtiFLAG.shape,year)

    gtiFLAG = pd.merge(gtiFLAG, dfgti, left_index = True, right_index = True, how = 'outer')  # index by naive times. how = 'inner': index by recorded times.
    print('MERGE gtiFLAG.shape =', gtiFLAG.shape,year)
    for column in gti:
        conditions = [gtiFLAG[column].isna(), 
                      gtiFLAG[column]== -9999, 
                      gtiFLAG[column] < gtiFLAG['PPmin'],
                      gtiFLAG[column] > gtiFLAG['PPmax']]
        flagcolumn = 'F_'+column
        gtiFLAG[flagcolumn] = np.select(conditions, flags, 0)
        gtiflagcount[column]= gtiFLAG[flagcolumn].value_counts()
    
#    gtiFLAG['sumflags']= gtiFLAG[fgti].sum() #   fix!!! dfgti['sumflags']= dfgti.iloc[:,4:8].sum(axis=1)
#   gtiSF = gtiFLAG['sumflags'].value_counts()
    
    gtiFLAG.to_pickle(BSRN_path + year +'gtiFLAG.pkl')
    gtiflagcount.to_csv(BSRN_path + year +'gtiflagcount.csv')
#   gtiSF.to_pickle(BSRN_path + year +'gtiSUMGFLAG.pkl')

 
    gtiFLAG = {}
  
print('END')

    
    

