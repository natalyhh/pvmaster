## STEP 5 - OIE VS INVERTERS

from types import CodeType
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib   # v 0.7.2

figs_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/INVERTER/figs/"
inv_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/INVERTER/"
gti_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNminGTI/"
ghi_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/BSRNmin/"

#location = pvlib.location.Location(-27.430891, -48.441406, tz = 'Etc/GMT', altitude= 2.74, name = 'Florianopolis')  # check for daylight savings 'Etc/GMT-3' 'Brazil/East' 'America/Sao_Paulo'

tzBRA = 'Etc/GMT+3'
tzETC = 'Etc/GMT-0'
                   
dcac = ['P_in1', 
        'P_grid',
        'I_in1']

GHIsensor = ['GHIP_SMP11',
             'F_GHIP_SMP11']

GTIsensor = ['TGIP_SMP11_VENT',
             'F_TGIP_SMP11_VENT']

   

#months = ['2018-01','2018-02','2018-03', '2018-04','2018-05','2018-06','2018-07','2018-08', '2018-09','2018-10','2018-11','2018-12',
#          '2019-01','2019-02','2019-03', '2019-04','2019-05','2019-06','2019-07','2019-08', '2019-09','2019-10','2019-11','2019-12',
#          '2020-01','2020-02','2020-03', '2020-04','2020-05','2020-06','2020-07','2020-08', '2020-09','2020-10','2020-11','2020-12',
#          '2021-01']

## The procedure below was needed because on 27/11/18, the inverter datalogger was synchronized with the meteostation, thus changing from GMT-3 to GMT-00. 
# This will allow direct comparison with irradiance timestamps.

dfCDT  = pd.read_csv(inv_path + 'CDT.csv') 
dfCDT['TIMESTAMP'] = dfCDT['TIMESTAMP'].astype(np.datetime64)
dfCDT = dfCDT.drop_duplicates(subset=['TIMESTAMP'])
dfCDT = dfCDT.set_index('TIMESTAMP')
#dfCDT = dfCDT.index.drop_duplicates()
dfCDTnosync = dfCDT[dfCDT.index < '2018-11-27 00:00:00']  # this part is in BRT (GMT - 3)
dfCDTnosync.index = dfCDTnosync.index.tz_localize(tzBRA)
dfCDTnosync.index = dfCDTnosync.index.tz_convert(tzETC)
dfCDTsync = dfCDT[dfCDT.index > '2018-11-28 00:00:00']  #  # this part is in  (GMT - 0)
dfCDTsync.index = dfCDTsync.index.tz_localize(tzETC)
dfCDTsync = [dfCDTnosync, dfCDTsync]
dfCDTsync = pd.concat(dfCDTsync)
dfPCDT = dfCDTsync[dcac]
dfPCDT = dfPCDT.loc['2018-01-01 00:00:00':'2021-01-01 00:00:00']
dfPCDT = dfPCDT.rename(columns={"P_in1": "Pdccdt", "I_in1": "Idccdt", "P_grid": "Paccdt"})
dfPCDT.shape

dfCDTA  = pd.read_csv(inv_path + 'CDTA.csv') 
dfCDTA['TIMESTAMP'] = dfCDTA['TIMESTAMP'].astype(np.datetime64)
dfCDTA = dfCDTA.drop_duplicates(subset=['TIMESTAMP'])
dfCDTA = dfCDTA.set_index('TIMESTAMP')
dfCDTAnosync = dfCDTA[dfCDTA.index < '2018-11-27 00:00:00']  # this part is in BRT (GMT - 3)
dfCDTAnosync.index = dfCDTAnosync.index.tz_localize(tzBRA)
dfCDTAnosync.index = dfCDTAnosync.index.tz_convert(tzETC)
dfCDTAsync = dfCDTA[dfCDTA.index > '2018-11-28 00:00:00']  #  # this part is in  (GMT - 0)
dfCDTAsync.index = dfCDTAsync.index.tz_localize(tzETC)
dfCDTAsync = [dfCDTAnosync, dfCDTAsync]
dfCDTAsync = pd.concat(dfCDTAsync)
dfPCDTA = dfCDTAsync[dcac]
dfPCDTA = dfPCDTA.loc['2018-01-01 00:00:00':'2021-01-01 00:00:00']
dfPCDTA = dfPCDTA.rename(columns={"P_in1": "Pdccdta", "I_in1": "Idccdta","P_grid": "Paccdta"})
dfPCDTA.shape



dfPSI  = pd.read_csv(inv_path + 'PSI.csv') 
dfPSI['TIMESTAMP'] = dfPSI['TIMESTAMP'].astype(np.datetime64)
dfPSI = dfPSI.drop_duplicates(subset=['TIMESTAMP'])
dfPSI = dfPSI.set_index('TIMESTAMP')
#dfPSI = dfPSI.index.drop_duplicates()
dfPSInosync = dfPSI[dfPSI.index < '2018-11-27 00:00:00']  # this part is in BRT (GMT - 3)
dfPSInosync.index = dfPSInosync.index.tz_localize(tzBRA)
dfPSInosync.index = dfPSInosync.index.tz_convert(tzETC)
dfPSIsync = dfPSI[dfPSI.index > '2018-11-28 00:00:00']  #  # this part is in  (GMT - 0)
dfPSIsync.index = dfPSIsync.index.tz_localize(tzETC)
dfPSIsync = [dfPSInosync, dfPSIsync]
dfPSIsync = pd.concat(dfPSIsync)
dfPPSI = dfPSIsync[dcac]
dfPPSI = dfPPSI.loc['2018-01-01 00:00:00':'2021-01-01 00:00:00']
dfPPSI = dfPPSI.rename(columns={"P_in1": "Pdcpsi", "I_in1": "Idcpsi","P_grid": "Pacpsi"})
dfPPSI.shape



pvsi = pd.merge(dfPCDT,dfPCDTA, how = 'left',left_index = True, right_index = True)
pvsi = pd.merge(pvsi,dfPPSI, how = 'left',left_index = True, right_index = True)

#############

dfgti18 = pd.read_pickle(gti_path + '2018' +'gtiFLAG.pkl')
dfgti19 = pd.read_pickle(gti_path + '2019' +'gtiFLAG.pkl')
dfgti20 = pd.read_pickle(gti_path + '2020' +'gtiFLAG.pkl')
dfgtis = [dfgti18[GTIsensor], dfgti19[GTIsensor], dfgti20[GTIsensor]]
dfgtis = pd.concat(dfgtis)
dfgtis = dfgtis[dfgtis.F_TGIP_SMP11_VENT < 4]

dfghi18 = pd.read_pickle(ghi_path + '2018' +'ghiFLAG.pkl')
dfghi19 = pd.read_pickle(ghi_path + '2019' +'ghiFLAG.pkl')
dfghi20 = pd.read_pickle(ghi_path + '2020' +'ghiFLAG.pkl')
dfghis = [dfghi18[GHIsensor], dfghi19[GHIsensor], dfghi20[GHIsensor]]
dfghis = pd.concat(dfghis)
dfghis = dfghis[dfghis.F_GHIP_SMP11 < 4]


dfirad = pd.merge(dfgtis,dfghis, how = 'inner',left_index = True, right_index = True)

pxir = pd.merge(pvsi,dfirad, how = 'inner',left_index = True, right_index = True)

pxir.to_pickle(inv_path  + 'PowervsIrrad.pkl')

#27/11/2018 - descartar este dia

oielist = [ '2018-01-11 15:54:00+00:00', '2018-12-15 14:35:00+00:00',  # ghi highest longest SiO2
            '2018-01-11 15:54:00+00:00', '2018-12-15 14:35:00+00:00',  # ghi highest longest SMP11 / SMP22
            '2018-12-15 14:35:00+00:00', '2018-12-15 14:29:00+00:00',  # ghi highest longest SPN1
            '2019-02-12 12:53:00+00:00', '2019-01-12 14:11:00+00:00',  # ghi highest longest SiO2 - SMP11 - SMP22 - SPN1
            '2019-01-16 15:17:00+00:00', # ghi second longest SPN1
            '2020-12-24 16:10:00+00:00', '2020-12-25 13:27:00+00:00',  # ghi highest longest SiO2
            '2020-12-24 16:10:00+00:00', '2020-01-07 15:22:00+00:00',  # ghi highest longest SMP11 / SMP22
            '2020-11-12 14:59:00+00:00',  # ghi highest longest SPN1
            '2018-02-14 15:35:00+00:00', '2018-02-16 15:02:00+00:00',  # gti highest longest SiO2 - SMP11
            '2019-02-12 15:30:00+00:00', '2019-01-12 14:11:00+00:00',  # gti highest longest SiO2 - really high here
            '2019-01-12 14:11:00+00:00', # gti highest and longest SMP11
            '2020-11-12 15:01:00+00:00', '2020-11-12 15:01:00+00:00',  # gti highest longest SiO2
            '2020-11-02 15:24:00+00:00', '2020-10-17 15:13:00+00:00',]   # gti highest longest SMP11 
          

#2020-11-19 12:42:00 - CdTe A
#2020-01-10 14:52:00	

#2020-01-10 11:50:00	- PSI
#2020-01-10 14:50:00	

#2020-11-19 12:42:00 - CDTE 	
#2020-11-19 15:42:00	


oielist = ['2020-01-10 14:52:00+00:00',	
           '2020-01-10 14:50:00+00:00',
           '2020-11-19 15:42:00+00:00']	#inverter highest dc power peaks
	

oielist = ['2019-02-05 14:25:00+00:00',	
           '2018-11-24 13:24:00+00:00',
           '2019-03-14 15:07:00+00:00']	#inverter worst eff    

oielist = ['2020-11-19 15:42:00+00:00',	
           '2020-01-10 14:51:00+00:00',
           '2019-09-23 16:15:00+00:00']   #inverter highest ac power peaks	

deltas = [5,30]

### PLOTS:

max_out = 2750
sc = 1361.1


for oie in oielist:
       for delta in deltas:
              event = pd.to_datetime(oie)
              start = event - datetime.timedelta(minutes=delta)
              end = event + datetime.timedelta(minutes=delta)

              fig, axes = plt.subplots(nrows=4,ncols=1, figsize=(20,10))

              f1= pxir['Pdccdt'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - CdTe')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l1.set_label('Max Output')
              axes[0].legend(loc='best')

              f2= pxir['Paccdt'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe')
              l2=axes[1].axhline(max_out,color='red',ls='--')
              l2.set_label('Max Output')
              axes[1].legend(loc='best')

              f3 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[2],color = 'orange',label='GTI - SMP11')
              l3=axes[2].axhline(sc,color='red',ls='--')
              l3.set_label('Solar Constant')
              axes[2].legend(loc='best')

              f4 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[3],color = 'salmon',label='GHI - SMP11')
              l4=axes[3].axhline(sc,color='red',ls='--')
              l4.set_label('Solar Constant')
              axes[3].legend(loc='best')

              figname =  figs_path + oie + 'd' + str(delta) + 'CdTe.jpeg'
              fig.savefig(figname)
              fig.clf()


              fig, axes = plt.subplots(nrows=4,ncols=1, figsize=(20,10))

              f1= pxir['Pdccdta'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - CdTe ARC')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l1.set_label('Max Output')
              axes[0].legend(loc='best')

              f2= pxir['Paccdta'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe ARC')
              l2=axes[1].axhline(max_out,color='red',ls='--')
              l2.set_label('Max Output')
              axes[1].legend(loc='best')

              f3 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[2],color = 'orange',label='GTI - SMP11')
              l3=axes[2].axhline(sc,color='red',ls='--')
              l3.set_label('Solar Constant')
              axes[2].legend(loc='best')

              f4 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[3],color = 'salmon',label='GHI - SMP11')
              l4=axes[3].axhline(sc,color='red',ls='--')
              l4.set_label('Solar Constant')
              axes[3].legend(loc='best')

              figname =  figs_path + oie + 'd' + str(delta) + 'CdTeA.jpeg'
              fig.savefig(figname)
              fig.clf()

              
              fig, axes = plt.subplots(nrows=4,ncols=1, figsize=(20,10))

              f1= pxir['Pdcpsi'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - mcSi')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l1.set_label('Max Output')
              axes[0].legend(loc='best')

              f2= pxir['Pacpsi'].loc[start:end].plot(ax=axes[1],label='AC Power - mcSi')
              l2=axes[1].axhline(max_out,color='red',ls='--')
              l2.set_label('Max Output')
              axes[1].legend(loc='best')

              f3 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[2],color = 'orange',label='GTI - SMP11')
              l3=axes[2].axhline(sc,color='red',ls='--')
              l3.set_label('Solar Constant')
              axes[2].legend(loc='best')

              f4 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[3],color = 'salmon',label='GHI - SMP11')
              l4=axes[3].axhline(sc,color='red',ls='--')
              l4.set_label('Solar Constant')
              axes[3].legend(loc='best')

              figname =  figs_path + oie + 'd'+ str(delta) + 'PSI.jpeg'
              fig.savefig(figname)
              fig.clf()

####PRINT THESE GRAPHS:








# calculate ILR during EOIE.

# compare model clearsky output vs EOIE Output

# what else could be done to access?

