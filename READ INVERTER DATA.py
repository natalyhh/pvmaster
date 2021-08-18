#  STEP 4 - READ INVERTER DATA - JULY/2021

from numba.core.extending import get_cython_function_address
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib   # v 0.7.2

main_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/INVERTER/"

pathCDT = "/Users/nataly/opt/AnacondaProjects/SAPIENS/original/GERACAO/CR1000-Sapiens_HT_SP1_INV_CDT.csv"
pathPSI = "/Users/nataly/opt/AnacondaProjects/SAPIENS/original/GERACAO/CR1000-Sapiens_HT_SP1_INV_PSI.csv"


varCDT =['TIMESTAMP',
         'INV_CDTE_231',
         'INV_CDTE_236',
         'INV_CDTE_237',
         'INV_CDTE_238',
         'INV_CDTE_239',
         'INV_CDTE_240',
         'INV_CDTE_241',
         'INV_CDTE_242',
         'INV_CDTE_243',
         'INV_CDTE_244',
         'INV_CDTE_245',
         'INV_CDTE_246',
         'INV_CDTE_247',
         'INV_CDTE_248']


varCDTA = ['TIMESTAMP',
           'INV_CDTE_331',
           'INV_CDTE_336',
           'INV_CDTE_337',
           'INV_CDTE_338',
           'INV_CDTE_339',
           'INV_CDTE_340',
           'INV_CDTE_341',
           'INV_CDTE_342',
           'INV_CDTE_343',
           'INV_CDTE_344',
           'INV_CDTE_345',
           'INV_CDTE_346',
           'INV_CDTE_347',
           'INV_CDTE_348']

varPSI = ['TIMESTAMP',
          'INV_PSI_431',
          'INV_PSI_436',
          'INV_PSI_437',
          'INV_PSI_438',
          'INV_PSI_439',
          'INV_PSI_440',
          'INV_PSI_441',
          'INV_PSI_442',
          'INV_PSI_443',
          'INV_PSI_444',
          'INV_PSI_445',
          'INV_PSI_446',
          'INV_PSI_447',
          'INV_PSI_448']


column_names = ['TIMESTAMP',
                   'E_tot',
                   'V_grid',
                   'I_grid',
                   'P_grid',
                   'F_grid',
                   'P_in1',
                   'V_in1',
                   'I_in1',
                   'P_in2',
                   'V_in2',
                   'I_in2',
                   'T_inverter',
                   'T_booster',
                   'R_iso'] 

grid = ['V_grid',
        'I_grid',
        'P_grid',
        'F_grid']

input1 = ['P_in1',
          'V_in1',
          'I_in1',]


input2 = ['P_in2',
          'V_in2',
          'I_in2',]

inverter = ['E_tot',
            'T_inverter',
            'T_booster',
            'R_iso']
                   
months = ['2018-01','2018-02','2018-03', '2018-04','2018-05','2018-06','2018-07','2018-08', '2018-09','2018-10','2018-11','2018-12',
          '2019-01','2019-02','2019-03', '2019-04','2019-05','2019-06','2019-07','2019-08', '2019-09','2019-10','2019-11','2019-12',
          '2020-01','2020-02','2020-03', '2020-04','2020-05','2020-06','2020-07','2020-08', '2020-09','2020-10','2020-11','2020-12',
          '2021-01']


dfCDT  = pd.read_csv(pathCDT, usecols=varCDT)
dfCDT.columns = column_names
print(dfCDT.shape)
dfCDT['TIMESTAMP'] = dfCDT['TIMESTAMP'].astype(np.datetime64)
dfCDT = dfCDT.fillna(-9999)
dfCDT = dfCDT.sort_values(by=['TIMESTAMP'])
dfCDT= dfCDT.drop_duplicates()
dfCDT = dfCDT.set_index('TIMESTAMP')
print(dfCDT.shape)


dfCDTA = pd.read_csv(pathCDT, usecols=varCDTA)
dfCDTA.columns = column_names
print(dfCDTA.shape)
dfCDTA['TIMESTAMP'] = dfCDTA['TIMESTAMP'].astype(np.datetime64)
dfCDTA = dfCDTA.fillna(-9999)
dfCDTA = dfCDTA.sort_values(by=['TIMESTAMP'])
dfCDTA= dfCDTA.drop_duplicates()
dfCDTA = dfCDTA.set_index('TIMESTAMP')
print(dfCDTA.shape)


dfPSI  = pd.read_csv(pathPSI, usecols=varPSI)
dfPSI.columns = column_names
print(dfPSI.shape)
dfPSI['TIMESTAMP'] = dfPSI['TIMESTAMP'].astype(np.datetime64)
dfPSI = dfPSI.fillna(-9999)
dfPSI = dfPSI.sort_values(by=['TIMESTAMP'])
dfPSI= dfPSI.drop_duplicates()
dfPSI = dfPSI.set_index('TIMESTAMP')
print(dfPSI.shape)

                 

cdtgrid      = dfCDT[grid]  
cdtin1       = dfCDT[input1]
cdtin2       = dfCDT[input2]
cdtinverter   = dfCDT[inverter]

cdtagrid      = dfCDTA[grid]  
cdtain1       = dfCDTA[input1]
cdtain2       = dfCDTA[input2]
cdtainverter   = dfCDTA[inverter]

psigrid      = dfPSI[grid]  
psiin1       = dfPSI[input1]
psiin2       = dfPSI[input2]
psiinverter   = dfPSI[inverter]

for month in months:
    cdtgridplot = cdtgrid.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTe - Grid '+ month+'.jpeg'
    fig = cdtgridplot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    
    cdtin1plot = cdtin1.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTe - Input 1 '+ month+'.jpeg'
    fig = cdtin1plot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    cdtin2plot = cdtin2.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTe - Input 2 '+ month+'.jpeg'
    fig = cdtin2plot[0].get_figure()
    fig.savefig(figname)
    fig.clf()


    cdtinverterplot = cdtinverter.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTe - Inverter '+ month+'.jpeg'
    fig = cdtinverterplot[0].get_figure()
    fig.savefig(figname)
    fig.clf()


    cdtagridplot = cdtagrid.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTeA - Grid '+ month+'.jpeg'
    fig = cdtagridplot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    cdtain1plot = cdtain1.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTeA - Input 1 '+ month+'.jpeg'
    fig = cdtain1plot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    cdtain2plot = cdtain2.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTeA - Input 2 '+ month+'.jpeg'
    fig = cdtain2plot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    cdtainverterplot = cdtainverter.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'CdTeA - Inverter '+ month+'.jpeg'
    fig = cdtainverterplot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    psigridplot = psigrid.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'PSI - Grid '+ month+'.jpeg'
    fig = psigridplot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    psiin1plot = psiin1.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'PSI - Input 1 '+ month+'.jpeg'
    fig = psiin1plot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    psiin2plot = psiin2.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'PSI - Input 2 '+ month+'.jpeg'
    fig = psiin2plot[0].get_figure()
    fig.savefig(figname)
    fig.clf()

    psiinverterplot = psiinverter.loc[month].plot(subplots=True, figsize=(20, 30))
    figname = 'PSI - Inverter '+ month+'.jpeg'
    fig = psiinverterplot[0].get_figure()
    fig.savefig(figname)
    fig.clf()


    dfCDT.to_csv(main_path + 'CDT.csv')     ### WHEN READ AGAIN NEED TO USE!!!!  ghiBRA.index = ghiBRA.index.tz_convert(tzBRA)
    dfCDTA.to_csv(main_path + 'CDTA.csv')   ### WHEN READ AGAIN NEED TO USE!!!!  ghiBRA.index = ghiBRA.index.tz_convert(tzBRA)
    dfPSI.to_csv(main_path + 'PSI.csv')     ### WHEN READ AGAIN NEED TO USE!!!!  ghiBRA.index = ghiBRA.index.tz_convert(tzBRA)
