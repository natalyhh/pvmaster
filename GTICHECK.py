#STEP 2.4 - QUALITY CHECK FOR GTI - 1 MINUTE DATA - DESCRIPTION AT THE END OF PAGE - JULY / 2021
# 2.3.1 is missing which is for second data.

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib   # v 0.7.2

main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/" 

BSRNm_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNmin/" 

# directory to save BSRN test results
GTI_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/GTIcheck/" 

ghi =  ['GHIP_SI02pt100',
        'GHIP_SMP11',
        'GHIP_SMP22',
        'GHIP_SPN1',
        'GHIT_SMP22'
        ]

gti = ['TGHIP_SI02pt100', 
       'TGHIP_SI02pt100_dirty',
       'TGIP_SMP11_VENT'
       ]
      
dif = ['DfHIP_SPN1', 
       'DfHIRP_SMP11',
       'DfHIT_SMP22',
       ]



dni = ['DNI_SHP1']

months = ['2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09', '2018-10', '2018-11', '2018-12',
          '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09', '2019-10', '2019-11', '2019-12',
          '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09', '2020-10', '2020-11', '2020-12',
          '2021-01']

years = ['2018', '2019', '2020', '2021']


# latitude, longitude, name, altitude, timezone - data retrieved in ETC/GMT - as plotted = noon around 3 pm
location = pvlib.location.Location(
            -27.430891, 
            -48.441406, 
            tz = 'Etc/GMT',    # check for daylight savings 'Etc/GMT-3' 'Brazil/East' 'America/Sao_Paulo'
            altitude= 2.74, 
            name = 'Florianopolis'
            )  

#PLANE OF INCIDENCE for sensors:
sensor_tilt = 27
sensor_azimuth = 0


naive_times = pd.date_range(start='2021-01', end='2021-02', freq='1Min')
times = naive_times.tz_localize(location.tz)  


solpos = pd.read_pickle(BSRNm_path+'2021solpos.pkl')

ghi = pd.read_pickle(main_path+'2021GHI.pkl')
dif = pd.read_pickle(main_path+'2021DIF.pkl')
dni = pd.read_pickle(main_path+'2021DNI.pkl')



'''ghi = pd.read_pickle(BSRNm_path+'2021ghiFLAG.pkl')
dif = pd.read_pickle(BSRNm_path+'2021difFLAG.pkl')
dni = pd.read_pickle(BSRNm_path+'2021dniFLAG.pkl')

#### NEED TO FIGURE OUT A WAY TO FILTER ONLY THE GOOD BSRN PASS DATA AND THEN PUT ALL VARIABLES WITH SAME LENGTH PROBABLY MERGE WITH  INTERSECTION ##### '''



irrad = pd.read_pickle(main_path+'IRRADIANCES.pkl')


 #solpos = pvlib.solarposition.get_solarposition(
 #       time      = weather.index,
 #       latitude  = location.latitude,
 #       longitude = location.longitude,
 #       altitude  = location.altitude,
 #       temperature = weather["temp_air"],
 #       pressure=pvlib.atmosphere.alt2pres(location.altitude)
 # )

    
dni_extra = pvlib.irradiance.get_extra_radiation(solpos.index)
airmass   = pvlib.atmosphere.get_relative_airmass(solpos['apparent_zenith'])
pressure  = pvlib.atmosphere.alt2pres(location.altitude)
am_abs    = pvlib.atmosphere.get_absolute_airmass(airmass, pressure)
    

total_irradianceKS = pvlib.irradiance.get_total_irradiance(
    sensor_tilt,
    sensor_azimuth,
    solpos['apparent_zenith'],
    solpos['azimuth'],
    dni.DNI_SHP1,
    ghi.GHIP_SMP22,
    dif.DfHIRP_SMP11,
    dni_extra = dni_extra,
    model='reindl',    #USE HDKR - CITE GUEYMARD ON OIE MODELLING - COULD EVEN USE OTHERS TO COMPARE
    )

total_irradianceSPN1 = pvlib.irradiance.get_total_irradiance(
    sensor_tilt,
    sensor_azimuth,
    solpos['apparent_zenith'],
    solpos['azimuth'],
    dni.DNI_SHP1,
    ghi.GHIP_SPN1,
    dif.DfHIRP_SPN1,
    dni_extra = dni_extra,
    model='reindl',    #USE HDKR - CITE GUEYMARD ON OIE MODELLING - COULD EVEN USE OTHERS TO COMPARE
    )
