#STEP 2.2 - BSRN TEST - 1 MINUTE DATA - DESCRIPTION AT THE END OF PAGE - JULY / 2021

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib  # v 0.7.2

# directory with clean and organized data per year for GHI, GTI, DIF, DNI
main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/CLEAN/" 

# directory to save BSRN test results
BSRN_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNmin/" 

ghi =  ['GHIP_SI02pt100',
        'GHIP_SMP11',
        'GHIP_SMP22',
        'GHIP_SPN1',
        'GHIT_SMP22']

fghi = ['F_GHIP_SI02pt100', 
        'F_GHIP_SMP11', 
        'F_GHIP_SMP22', 
        'F_GHIP_SPN1', 
        'F_GHIT_SMP22']

gti = ['TGHIP_SI02pt100', 
       'TGHIP_SI02pt100_dirty',
       'TGIP_SMP11_VENT']
      
dif = ['DfHIP_SPN1', 
       'DfHIRP_SMP11',
       'DfHIT_SMP22',
       'DIF_GLO_REF_SPN1']

fdif = ['F_DfHIP_SPN1', 
        'F_DfHIRP_SMP11', 
        'F_DfHIT_SMP22',
        'F_DIF_GLO_REF_SPN1']

dni = ['DNI_SHP1']

fdni = ['F_DNI_SHP1']

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

PPmin = -4  # minimum physically possible limit
ERmin = -2  # minimum extremely rare limit

flags = [-1, #NaN
         -1, #-9999   - apparently did not appear?!?! TEST: create specific flag to track it.
          3, # too low PP
          1, # too low ER
          2, # too high ER
          4] # too high PP

ghiflagcount = pd.DataFrame(columns= [ghi], index = [-1, 0, 1, 2, 3, 4], dtype = int) 
difflagcount = pd.DataFrame(columns= [dif], index = [-1, 0, 1, 2, 3, 4], dtype = int) 
dniflagcount = pd.DataFrame(columns= [dni], index = [-1, 0, 1, 2, 3, 4], dtype = int) 


#### end definitions

for year in years:
    ghiFLAG = pd.DataFrame(columns = ['PPmax', 'PPmin', 'ERmax', 'ERmin', 
                                      'F_GHIP_SI02pt100', 'F_GHIP_SMP11', 
                                      'F_GHIP_SMP22', 'F_GHIP_SPN1', 'F_GHIT_SMP22'])
    difFLAG = pd.DataFrame(columns = ['PPmax', 'PPmin', 'ERmax', 'ERmin', 
                                      'F_DfHIP_SPN1', 'F_DfHIRP_SMP11', 
                                      'F_DfHIT_SMP22', 'F_DIF_GLO_REF_SPN1'])  
    dniFLAG = pd.DataFrame(columns = ['PPmax', 'PPmin', 'ERmax', 'ERmin', 'F_DNI_SHP1'])
    
    dfghi = pd.read_pickle(main_path+year+'GHI.pkl')
    dfghi = dfghi.resample('1Min').mean()  
    print('dfghi.shape =', dfghi.shape,year)


    dfgti = pd.read_pickle(main_path+year+'GTI.pkl')
    dfgti = dfgti.resample('1Min').mean()  

    dfdif = pd.read_pickle(main_path+year+'DIF.pkl')
    dfdif = dfdif.resample('1Min').mean()  

    dfdni = pd.read_pickle(main_path+year+'DNI.pkl')
    dfdni = dfdni.resample('1Min').mean()  

    dfghi.index = dfghi.index.tz_localize(location.tz)
    dfgti.index = dfgti.index.tz_localize(location.tz)
    dfdif.index = dfdif.index.tz_localize(location.tz)
    dfdni.index = dfdni.index.tz_localize(location.tz)

    naive_times = pd.date_range(start = dfghi.index.min(), end = dfghi.index.max(), freq='1Min', tz = location.tz)
    naive_times = pd.DatetimeIndex(naive_times)   # PROBLEM: WILL HAVE TO DEAL WITH MISSING VALUES
    print('NAIVE.shape =', naive_times.shape,year)

    missing.loc[year] = (len(naive_times) - len(dfghi.index))/3600/24

    eth = pvlib.irradiance.get_extra_radiation(naive_times, solar_constant = 1366.1, method = 'nrel').to_frame()
    solpos = pvlib.solarposition.get_solarposition(naive_times, location.latitude, location.longitude, location.altitude, pressure = 101293, temperature = 25)

    cosSZA = np.cos(np.deg2rad(solpos.zenith)).to_frame()
   
    ghiFLAG['PPmax'] = eth[0]*1.5*(cosSZA.zenith**(1.2)) + 100   # PPMAX TOO LOW! CHECK PROBLEMS WITH CALCULATION
    ghiFLAG['PPmin'] = PPmin
    ghiFLAG['ERmax'] = eth[0]*1.2*(cosSZA.zenith**(1.2)) + 50
    ghiFLAG['ERmin'] = ERmin
    print('ghiFLAG.shape =', ghiFLAG.shape,year)


    difFLAG['PPmax'] = eth[0]*0.95*(cosSZA.zenith**(1.2))+ 50
    difFLAG['PPmin'] = PPmin
    difFLAG['ERmax'] = eth[0]*0.75*(cosSZA.zenith**(1.2))+ 30
    difFLAG['ERmin'] = ERmin
    
    dniFLAG['PPmax'] = eth[0]
    dniFLAG['PPmin'] = PPmin
    dniFLAG['ERmax'] = eth[0]*0.95*(cosSZA.zenith**(0.2)) +10
    dniFLAG['ERmin'] = ERmin

    ghiFLAG = pd.merge(ghiFLAG, dfghi, left_index = True, right_index = True, how = 'outer')  # index by naive times. how = 'inner': index by recorded times.
    difFLAG = pd.merge(difFLAG, dfdif, left_index = True, right_index = True, how='outer')  # index by naive times. how = 'inner': index by recorded times.
    dniFLAG = pd.merge(dniFLAG, dfdni, left_index = True, right_index = True, how='outer')  # index by naive times. how = 'inner': index by recorded times.
    print('MERGE ghiFLAG.shape =', ghiFLAG.shape,year)

    for column in ghi:
        conditions = [ghiFLAG[column].isna(), 
                      ghiFLAG[column]== -9999, 
                      ghiFLAG[column] < ghiFLAG['PPmin'],
                     (ghiFLAG[column] > ghiFLAG['PPmin']) & (ghiFLAG[column]< ghiFLAG['ERmin']),
                     (ghiFLAG[column] > ghiFLAG['ERmax']) & (ghiFLAG[column]< ghiFLAG['PPmax']),
                      ghiFLAG[column] > ghiFLAG['PPmax']]
        flagcolumn = 'F_'+column
        ghiFLAG[flagcolumn] = np.select(conditions, flags, 0)
        ghiflagcount[column]= ghiFLAG[flagcolumn].value_counts()
    
    ghiFLAG['sumflags']= ghiFLAG[fghi].sum() #   fix!!! dfghi['sumflags']= dfghi.iloc[:,4:8].sum(axis=1)
#   ghiSF = ghiFLAG['sumflags'].value_counts()
    
    ghiFLAG.to_pickle(BSRN_path + year +'ghiFLAG.pkl')
    ghiflagcount.to_csv(BSRN_path + year +'ghiflagcount.csv')
#   ghiSF.to_pickle(BSRN_path + year +'ghiSUMGFLAG.pkl')


    for column in dif:
        conditions = [difFLAG[column].isna(), 
                      difFLAG[column]== -9999, 
                      difFLAG[column] < difFLAG['PPmin'],
                     (difFLAG[column] > difFLAG['PPmin']) & (difFLAG[column]< difFLAG['ERmin']),
                     (difFLAG[column] > difFLAG['ERmax']) & (difFLAG[column]< difFLAG['PPmax']),
                      difFLAG[column] > difFLAG['PPmax']]
        flagcolumn = 'F_'+column
        difFLAG[flagcolumn] = np.select(conditions, flags, 0)
        difflagcount[column]= difFLAG[flagcolumn].value_counts()

    difFLAG['sumflags']= difFLAG[fdif].sum()
#   difSF = difFLAG['sumflags'].value_counts()

    difFLAG.to_pickle(BSRN_path + year +'difFLAG.pkl')
    difflagcount.to_csv(BSRN_path + year +'difflagcount.csv')
#   difSF.to_pickle(BSRN_path + year +'difSUMGFLAG.pkl')


    for column in dni:
        conditions = [dniFLAG[column].isna(), 
                      dniFLAG[column]== -9999, 
                      dniFLAG[column] < dniFLAG['PPmin'],
                     (dniFLAG[column] > dniFLAG['PPmin']) & (dniFLAG[column]< dniFLAG['ERmin']),
                     (dniFLAG[column] > dniFLAG['ERmax']) & (dniFLAG[column]< dniFLAG['PPmax']),
                      dniFLAG[column] > dniFLAG['PPmax']]
        flagcolumn = 'F_'+column
        dniFLAG[flagcolumn] = np.select(conditions, flags, 0)
        dniflagcount[column]= dniFLAG[flagcolumn].value_counts()

#    dniFLAG['sumflags']= dniFLAG[fdni].sum()
#    dniSF = dniFLAG['sumflags'].value_counts()    

    dniFLAG.to_pickle(BSRN_path + year +'dniFLAG.pkl')
    dniflagcount.to_csv(BSRN_path + year +'dniflagcount.csv')
#   dniSF.to_pickle(BSRN_path + year +'dniSUMGFLAG.pkl') 

    eth.to_pickle(BSRN_path + year + 'ETH.pkl')
    solpos.to_pickle(BSRN_path + year + 'solpos.pkl')
 
    ghiFLAG = {}
    difFLAG = {}
    dniFLAG = {}

missing.to_pickle(BSRN_path + 'rec_missing_days.pkl')

print('END')

    
    


### MAY NEED AVERAGE PER MINUTE FOR BETTER DATA



   




### GOALS 10/07/21 ###
# 1) SAVE CLEAR DATA PER YEAR - ok
#
# 2) BSRN - finish codng with sample: - ok
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
#  1 - too low  (CT)  - will not use
#  2 - too high (CT)  - will not use
#  3 - too low  (ER)  - shift: 1  
#  4 - too high (ER)  - shift: 2
#  5 - too low  (PP)  - shift: 3
#  6 - too high (PP)  - shift: 4
#
# REJECTED FLAGS: SET VALUE TO -1
# POSSIBLY AID ANALYSIS WITH PLOTS