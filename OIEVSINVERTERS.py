## STEP 5 - OIE VS INVERTERS

from types import CodeType
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetime
import pytz
import pvlib   # v 0.7.2

figs_path = "/Users/nataly/opt/AnacondaProjects/SAPIENS/INVERTER/figsfinal/"
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
dfPCDT.Idccdt = dfPCDT.Idccdt / 4
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
dfPCDTA.Idccdta = dfPCDTA.Idccdta / 4 
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

#pxir.to_pickle(inv_path  + 'PowervsIrrad.pkl')

#27/11/2018 - descartar este dia

oielist = [ '2018-01-11 15:54:00+00:00', '2018-12-15 14:35:00+00:00',  # ghi highest longest SiO2
            '2018-01-11 15:54:00+00:00', '2018-12-15 14:35:00+00:00',  # ghi highest longest SMP11 / SMP22
            '2018-12-15 14:35:00+00:00', '2018-12-15 14:29:00+00:00',  # ghi highest longest SPN1
            '2019-02-12 12:53:00+00:00', '2019-01-12 14:11:00+00:00',  # ghi highest longest SiO2 - SMP11 - SMP22 - SPN1
            '2019-01-16 15:17:00+00:00', # ghi second longest SPN1
            '2020-12-24 16:10:00+00:00', '2020-12-25 13:27:00+00:00',  # ghi highest longest SiO2
            '2020-12-24 16:10:00+00:00', '2020-01-07 15:22:00+00:00',  # ghi highest longest SMP11 / SMP22
            '2020-11-12 14:59:00+00:00',]  # ghi highest longest SPN1



'''oielist = [ '2018-02-14 15:35:00+00:00', '2018-02-16 15:02:00+00:00',  # gti highest longest SiO2 - SMP11
            '2019-02-12 15:30:00+00:00', '2019-01-12 14:11:00+00:00',  # gti highest longest SiO2 - really high here
            '2019-01-12 14:11:00+00:00', # gti highest and longest SMP11
            '2020-11-12 15:01:00+00:00', '2020-11-12 15:01:00+00:00',  # gti highest longest SiO2
            '2020-11-02 15:24:00+00:00', '2020-10-17 15:13:00+00:00']   # gti highest longest SMP11    - INCLUDED IN MASTER THESIS'''
          

#2020-11-19 12:42:00 - CdTe A
#2020-01-10 14:52:00	

#2020-01-10 11:50:00	- PSI
#2020-01-10 14:50:00	

#2020-11-19 12:42:00 - CDTE 	
#2020-11-19 15:42:00	

#### INTERRESTING EVENTS:
'''
oielist  = ['2020-01-10 14:52:00+00:00',	
             '2020-01-10 14:50:00+00:00',
             '2020-11-19 15:42:00+00:00']	#inverter highest dc power peaks'''
	

#oielist3 = ['2019-02-05 14:25:00+00:00',	
        #   '2018-11-24 13:24:00+00:00',
         #  '2019-03-14 15:07:00+00:00']	#inverter worst efficiency    

'''oielist = ['2020-11-19 15:42:00+00:00',	
           '2020-01-10 14:51:00+00:00',
           '2019-09-23 16:15:00+00:00']   #inverter highest ac power peaks	- INCLUDED IN MASTER THESIS'''


'''
oielist = ['2019-04-24 15:00:00+00:00',
           '2019-01-20 15:00:00+00:00',] # MAX GHI PV CAMPER '''

'''
oielist = ['2019-09-23 15:00:00+00:00',
           '2019-03-11 15:00:00+00:00',]  #MAX GTI PVCAMPER '''

'''

oielist = [   '2019-01-12 14:11:00+00:00',  ### GHI CORRECT 24-08-21
              '2019-02-12 12:53:00+00:00',
              '2018-01-11 15:54:00+00:00',
              '2020-11-12 14:59:00+00:00',
              '2018-12-15 14:35:00+00:00',
              '2019-01-12 14:11:00+00:00',
              '2020-12-24 16:10:00+00:00',
              '2019-01-16 15:08:00+00:00',
              '2020-11-22 13:29:00+00:00',
              '2019-02-02 15:20:00+00:00',
              '2020-10-31 15:04:00+00:00',
              '2020-01-07 15:21:00+00:00',
              '2020-12-25 13:26:00+00:00',
              '2020-01-21 13:47:00+00:00',
              '2020-10-17 15:13:00+00:00',
              '2018-01-17 13:18:00+00:00',
              '2019-06-25 15:43:00+00:00',
              '2018-02-05 11:52:00+00:00',
              '2018-10-11 11:13:00+00:00',
              '2019-02-21 11:09:00+00:00',
              '2019-02-25 20:32:00+00:00',
              '2018-02-03 09:51:00+00:00'] '''

'''
oielist =    ['2018-11-09 14:57:00+00:00',
              '2018-03-03 15:11:00+00:00',  #cdta - 0.88
              '2019-01-25 16:39:00+00:00',  #cdta - 0.915
              '2019-11-24 14:25:00+00:00']  ## cdta  0.89 '''


'''
oielist = ['2020-10-16 13:56:00+00:00',
           '2018-03-03 15:11:00+00:00',
           '2020-11-03 14:35:00+00:00']  # EOIE loweest inverter efficiency '''


'''oielist = ['2018-02-16 15:07:00+00:00',
           '2018-01-15 16:10:00+00:00',
           '2018-01-15 15:30:00+00:00' ] # max currents
'''


deltas = [30]
max_out = 2750
max_nom = 2500
sc = 1361.1
#fuse = 4

### PLOTS - POWER DC AC GHI GTI:

'''
for oie in oielist:
       for delta in deltas:
              event = pd.to_datetime(oie)
              start = event - datetime.timedelta(minutes=delta)
              end = event + datetime.timedelta(minutes=delta)

              fig, axes = plt.subplots(nrows=4,ncols=1, figsize=(20,10))

              f1= pxir['Pdccdt'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - CdTe')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l11=axes[0].axhline(max_nom,color='pink',ls='--')
              l1.set_label('Max Output')
              l11.set_label('Nominal')
              axes[0].legend(loc='best')

              f2= pxir['Paccdt'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe')
              l2=axes[1].axhline(max_out,color='red',ls='--')
              l21=axes[1].axhline(max_nom,color='pink',ls='--')
              l21.set_label('Nominal')
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
              l11=axes[0].axhline(max_nom,color='pink',ls='--')
              l11.set_label('Nominal')
              axes[0].legend(loc='best')

              f2= pxir['Paccdta'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe ARC')
              l2=axes[1].axhline(max_out,color='red',ls='--')
              l2.set_label('Max Output')
              l21=axes[1].axhline(max_nom,color='pink',ls='--')
              l21.set_label('Nominal')
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
              l11=axes[0].axhline(max_nom,color='pink',ls='--')
              l11.set_label('Nominal')
              axes[0].legend(loc='best')

              f2= pxir['Pacpsi'].loc[start:end].plot(ax=axes[1],label='AC Power - mcSi')
              l2=axes[1].axhline(max_out,color='red',ls='--')
              l2.set_label('Max Output')
              l21=axes[1].axhline(max_nom,color='pink',ls='--')
              l21.set_label('Nominal')
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
'''

### PLOTS -  P_DC I_DC P_AC GHI:
'''  

for oie in oielist:
       for delta in deltas:
              event = pd.to_datetime(oie)
              start = event - datetime.timedelta(minutes=delta)
              end = event + datetime.timedelta(minutes=delta)

            fig, axes = plt.subplots(nrows=3,ncols=1, figsize=(20,10))#

              f1= pxir['Pdccdt'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - CdTe')
              f2= pxir['Paccdt'].loc[start:end].plot(ax=axes[0],label='AC Power - CdTe')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l1.set_label('Max Output')
              l11=axes[0].axhline(max_nom,color='pink',ls='--')
              l11.set_label('Nominal')
              axes[0].legend(loc='lower left')

              #f2= pxir['Paccdt'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe')
              #l2=axes[1].axhline(max_out,color='red',ls='--')
              #l2.set_label('Max Output')
              #l21=axes[1].axhline(max_nom,color='pink',ls='--')
              #l21.set_label('Nominal')
              #axes[1].legend(loc='lower left')

              f3 = pxir['Idccdt'].loc[start:end].plot(ax=axes[1],color = 'purple',label='DC Current - CdTe')
              l3=axes[1].axhline(4,color='red',ls='--')
              l3.set_label('Fuse rating')
              axes[1].legend(loc='lower left')

              f4 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[2],color = 'salmon',label='GHI - SMP11')
              f5 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[2],color = 'orange',label='GTI - SMP11')
              l4=axes[2].axhline(sc,color='red',ls='--')
              l4.set_label('Solar Constant')
              axes[2].legend(loc='lower left')

              figname =  figs_path + oie + 'CdTe.jpeg'
              fig.savefig(figname)
              fig.clf()


              fig, axes = plt.subplots(nrows=3,ncols=1, figsize=(20,10))

              f1= pxir['Pdccdta'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - CdTe ARC')
              f2= pxir['Paccdta'].loc[start:end].plot(ax=axes[0],label='AC Power - CdTe ARC')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l1.set_label('Max Output')
              l11=axes[0].axhline(max_nom,color='pink',ls='--')
              l11.set_label('Nominal')
              axes[0].legend(loc='lower left')

              #f2= pxir['Paccdta'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe ARC')
              #l2=axes[1].axhline(max_out,color='red',ls='--')
              #l2.set_label('Max Output')
              #l21=axes[1].axhline(max_nom,color='pink',ls='--')
              #l21.set_label('Nominal')
              #axes[1].legend(loc='lower left')

              f3 = pxir['Idccdta'].loc[start:end].plot(ax=axes[1],color = 'purple',label='DC Current - CdTe ARC')
              l3=axes[1].axhline(4,color='red',ls='--')
              l3.set_label('Fuse rating')
              axes[1].legend(loc='lower left')

              f4 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[2],color = 'salmon',label='GHI - SMP11')
              f5 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[2],color = 'orange',label='GTI - SMP11')
              l4=axes[2].axhline(sc,color='red',ls='--')
              l4.set_label('Solar Constant')
              axes[2].legend(loc='lower left')

              figname =  figs_path + oie + 'CdTeA.jpeg'
              fig.savefig(figname)
              fig.clf()

              
              fig, axes = plt.subplots(nrows=3,ncols=1, figsize=(20,10))

              f1= pxir['Pdcpsi'].loc[start:end].plot(ax=axes[0],color = 'green',label='DC Power - mcSi')
              f2= pxir['Pacpsi'].loc[start:end].plot(ax=axes[0],label='AC Power - mcSi')
              l1=axes[0].axhline(max_out,color='red',ls='--')
              l1.set_label('Max Output')
              l11=axes[0].axhline(max_nom,color='pink',ls='--')
              l11.set_label('Nominal')
              axes[0].legend(loc='lower left')

             # f2= pxir['Pacpsi'].loc[start:end].plot(ax=axes[1],label='AC Power - mcSi')
             # l2=axes[1].axhline(max_out,color='red',ls='--')
             # l2.set_label('Max Output')
             # l21=axes[1].axhline(max_nom,color='pink',ls='--')
             # l21.set_label('Nominal')
             # axes[1].legend(loc='lower left')

              f3 = pxir['Idcpsi'].loc[start:end].plot(ax=axes[1],color = 'purple',label='DC Current - mc Si')
              l3=axes[1].axhline(15,color='red',ls='--')
              l3.set_label('Fuse rating')
              axes[1].legend(loc='lower left')


              f4 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[2],color = 'salmon',label='GHI - SMP11')
              f5 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[2],color = 'orange',label='GTI - SMP11')
              l4=axes[2].axhline(sc,color='red',ls='--')
              l4.set_label('Solar Constant')
              axes[2].legend(loc='lower left')

              figname =  figs_path + oie + 'PSI.jpeg'
              fig.savefig(figname)
              fig.clf()



'''



for oie in oielist:
       for delta in deltas:
              event = pd.to_datetime(oie)
              start = event - datetime.timedelta(minutes=delta)
              end = event + datetime.timedelta(minutes=delta)
             
              fig, axes = plt.subplots(nrows=7,ncols=1, figsize=(20,30))#

              f11 = pxir['GHIP_SMP11'].loc[start:end].plot(ax=axes[0],color = 'salmon',label='GHI - SMP11')
              f12 = pxir['TGIP_SMP11_VENT'].loc[start:end].plot(ax=axes[0],color = 'orange',label='GTI - SMP11')
              l1=axes[0].axhline(sc,color='red',ls='--')
              l1.set_label('Solar Constant')
              axes[0].legend(loc='lower left')


              f21= pxir['Pdccdt'].loc[start:end].plot(ax=axes[1],color = 'green',label='DC Power - CdTe')
              f22= pxir['Paccdt'].loc[start:end].plot(ax=axes[1],label='AC Power - CdTe')
              l21=axes[1].axhline(max_out,color='red',ls='--')
              l21.set_label('Max P Output')
              l22=axes[1].axhline(max_nom,color='pink',ls='--')
              l22.set_label('Nominal')
              axes[1].legend(loc='lower left')

              f31= pxir['Pdccdta'].loc[start:end].plot(ax=axes[2],color = 'green',label='DC Power - CdTe ARC')
              f32= pxir['Paccdta'].loc[start:end].plot(ax=axes[2],label='AC Power - CdTe ARC')
              l31=axes[2].axhline(max_out,color='red',ls='--')
              l31.set_label('Max P Output')
              l32=axes[2].axhline(max_nom,color='pink',ls='--')
              l32.set_label('Nominal')
              axes[2].legend(loc='lower left')


              f41= pxir['Pdcpsi'].loc[start:end].plot(ax=axes[3],color = 'green',label='DC Power - mcSi')
              f42= pxir['Pacpsi'].loc[start:end].plot(ax=axes[3],label='AC Power - mcSi')
              l41=axes[3].axhline(max_out,color='red',ls='--')
              l41.set_label('Max P Output')
              l42=axes[3].axhline(max_nom,color='pink',ls='--')
              l42.set_label('Nominal')
              axes[3].legend(loc='lower left')


              f51 = pxir['Idccdt'].loc[start:end].plot(ax=axes[4],color = 'purple',label='DC Current - CdTe')
              l51=axes[4].axhline(4,color='red',ls='--')
              l51.set_label('Fuse rating')
              axes[4].legend(loc='lower left')

              f61 = pxir['Idccdta'].loc[start:end].plot(ax=axes[5],color = 'purple',label='DC Current - CdTe ARC')
              l61=axes[5].axhline(4,color='red',ls='--')
              l61.set_label('Fuse rating')
              axes[5].legend(loc='lower left')


              f71 = pxir['Idcpsi'].loc[start:end].plot(ax=axes[6],color = 'purple',label='DC Current - mc Si')
              l71=axes[6].axhline(15,color='red',ls='--')
              l71.set_label('Fuse rating')
              axes[6].legend(loc='lower left')




              figname =  figs_path + oie + '.jpeg'
              fig.savefig(figname)
              fig.clf()

              






# calculate ILR during EOIE.

# compare model clearsky output vs EOIE Output

# what else could be done to access?


##### INVESTIGATE TIME SHIFTS 

'''GHIsensor2 = ['GHIP_SI02pt100',
             'F_GHIP_SI02pt100']


dfghi18b = pd.read_pickle(ghi_path + '2018' +'ghiFLAG.pkl')
dfghi19b = pd.read_pickle(ghi_path + '2019' +'ghiFLAG.pkl')
dfghi20b = pd.read_pickle(ghi_path + '2020' +'ghiFLAG.pkl')
dfghisb = [dfghi18b[GHIsensor2], dfghi19b[GHIsensor2], dfghi20b[GHIsensor2]]
dfghisb = pd.concat(dfghisb)       
dfghisb.index.drop_duplicates()
dfiradb = pd.merge(dfghisb, how = 'left',left_index = True, right_index = True)
pxirb = pd.merge(pvsi,dfiradb, how = 'left',left_index = True, right_index = True)


dfshiftb = pd.DataFrame(columns = ['Pdccdta', 'ghi-5','ghi-4', 'ghi-3','ghi-2','ghi-1', 'ghi', 'ghi1','ghi2', 'ghi3','ghi4','ghi5'])
dfshiftb['Pdccdt'] = pxirb['Pdccdt']
dfshiftb['ghi']=pxirb['GHIP_SI02pt100']
dfshiftb.loc[:,'ghi1']= dfshiftb.ghi.shift(1)
dfshiftb.loc[:,'ghi2']= dfshiftb.ghi.shift(2)
dfshiftb.loc[:,'ghi3']= dfshiftb.ghi.shift(3)
dfshiftb.loc[:,'ghi4']= dfshiftb.ghi.shift(4)
dfshiftb.loc[:,'ghi5']= dfshiftb.ghi.shift(5)
dfshiftb.loc[:,'ghi-1']= dfshiftb.ghi.shift(-1)
dfshiftb.loc[:,'ghi-2']= dfshiftb.ghi.shift(-2)
dfshiftb.loc[:,'ghi-3']= dfshiftb.ghi.shift(-3)
dfshiftb.loc[:,'ghi-4']= dfshiftb.ghi.shift(-4)
dfshiftb.loc[:,'ghi-5']= dfshiftb.ghi.shift(-5)
dfshiftb.corr()

dfshiftAb = pd.DataFrame(columns = ['Pdccdta', 'ghi-5','ghi-4', 'ghi-3','ghi-2','ghi-1', 'ghi', 'ghi1','ghi2', 'ghi3','ghi4','ghi5'])
dfshiftAb['Pdccdta'] = pxirb['Pdccdta']
dfshiftAb['ghi']= pxirb['GHIP_SI02pt100']
dfshiftAb.loc[:,'ghi1']= dfshiftAb.ghi.shift(1)
dfshiftAb.loc[:,'ghi2']= dfshiftAb.ghi.shift(2)
dfshiftAb.loc[:,'ghi3']= dfshiftAb.ghi.shift(3)
dfshiftAb.loc[:,'ghi4']= dfshiftAb.ghi.shift(3)
dfshiftAb.loc[:,'ghi5']= dfshiftAb.ghi.shift(3)
dfshiftAb.loc[:,'ghi-1']= dfshiftAb.ghi.shift(-1)
dfshiftAb.loc[:,'ghi-2']= dfshiftAb.ghi.shift(-2)
dfshiftAb.loc[:,'ghi-3']= dfshiftAb.ghi.shift(-3)
dfshiftAb.loc[:,'ghi-4']= dfshiftAb.ghi.shift(-3)
dfshiftAb.loc[:,'ghi-5']= dfshiftAb.ghi.shift(-3)

dfshiftpsib = pd.DataFrame(columns = ['Pdcpsi', 'ghi-5','ghi-4', 'ghi-3','ghi-2','ghi-1', 'ghi', 'ghi1','ghi2', 'ghi3','ghi4','ghi5'])
dfshiftpsib['Pdcpsi'] = pxirb['Pdcpsi']
dfshiftpsib['ghi']=pxirb['GHIP_SI02pt100']
dfshiftpsib.loc[:,'ghi1']= dfshiftpsib.ghi.shift(1)
dfshiftpsib.loc[:,'ghi2']= dfshiftpsib.ghi.shift(2)
dfshiftpsib.loc[:,'ghi3']= dfshiftpsib.ghi.shift(3)
dfshiftpsib.loc[:,'ghi4']= dfshiftpsib.ghi.shift(4)
dfshiftpsib.loc[:,'ghi5']= dfshiftpsib.ghi.shift(5)
dfshiftpsib.loc[:,'ghi-1']= dfshiftpsib.ghi.shift(-1)
dfshiftpsib.loc[:,'ghi-2']= dfshiftpsib.ghi.shift(-2)
dfshiftpsib.loc[:,'ghi-3']= dfshiftpsib.ghi.shift(-3)
dfshiftpsib.loc[:,'ghi-4']= dfshiftpsib.ghi.shift(-4)
dfshiftpsib.loc[:,'ghi-5']= dfshiftpsib.ghi.shift(-5)

C1b = dfshiftb.corr()
C1b = C1b.iloc[0,:]
C1b = C1b.iloc[1:12]
C1b.index = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]


C2b = dfshiftAb.corr()
C2b = C2b.iloc[0,:]
C2b = C2b.iloc[1:12]
C2b.index = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]

C3b = dfshiftpsib.corr()
C3b = C3b.iloc[0,:]
C3b = C3b.iloc[1:12]
C3b.index = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5] '''


