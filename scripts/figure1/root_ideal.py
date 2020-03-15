# -*- coding: utf-8 -*-
#Ideal experiment for Fig1 with or without RFvolc of year 1964
import csv
import warnings
import time
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")

execfile('OSCAR.py')
data_RF_IPCC_orgin=np.array([line for line in csv.reader(open('RF_IPCC.csv','r'))],dtype=dty)
data_RF_IPCC=data_RF_IPCC_orgin

RF_List=['RF','RF_CO2','RF_CH4','RF_H2Os','RF_N2O','RF_halo',
         'RF_O3t','RF_O3s','RF_SO4','RF_POA','RF_BC','RF_NO3','RF_SOA',
         'RF_cloud','RF_BCsnow','RF_LCC']

N=2 #Monte Carlo
for n_run in range(N):
    execfile('ran_config.py')
    
    [RF,RF_CO2,RF_CH4,RF_H2Os,RF_N2O,RF_halo,
         RF_O3t,RF_O3s,RF_SO4,RF_POA,RF_BC,RF_NO3,RF_SOA,
         RF_cloud,RF_BCsnow,RF_LCC,D_gst,D_gyp]=OSCAR_lite(var_output=RF_List+['D_gst','D_gyp'])
    execfile('init_RF.py')
    the_year=1964
    execfile('init_RF.py')
    [D_gst,D_CO2,RF_CO2,LSNK,D_rh1,D_rh2,D_npp,D_AREA,OSNK,LSNK,D_FOUT,D_FIN]=OSCAR_lite(force_RFs=True,
        var_output=['D_gst','D_CO2','RF_CO2','LSNK','D_rh1','D_rh2','D_npp','D_AREA',
                    'OSNK','LSNK','D_FOUT','D_FIN'])
    RFvolc_tmp=RFvolc.copy()
    RFvolc_tmp[the_year-1700]*=0
    [D_gst_tmp,D_CO2_tmp,RF_CO2_tmp,LSNK_tmp,D_rh1_tmp,D_rh2_tmp,D_npp_tmp,D_AREA_tmp,OSNK_tmp,LSNK_tmp,D_FOUT_tmp,D_FIN_tmp]=OSCAR_lite(force_RFs=True
        ,var_output=['D_gst','D_CO2','RF_CO2','LSNK','D_rh1','D_rh2','D_npp','D_AREA','OSNK','LSNK','D_FOUT','D_FIN']
        ,RFvolc=RFvolc_tmp)
    D_RH=np.sum(np.sum((D_rh1 + D_rh2)*(AREA_0 + D_AREA),1),1)
    D_RH_tmp=np.sum(np.sum((D_rh1_tmp + D_rh2_tmp)*(AREA_0 + D_AREA_tmp),1),1)
    D_NPP=np.sum(np.sum((D_npp)*(AREA_0 + D_AREA),1),1)
    D_NPP_tmp=np.sum(np.sum((D_npp_tmp)*(AREA_0 + D_AREA_tmp),1),1)
    D_FOUT=np.sum(D_FOUT,1)
    D_FIN=np.sum(D_FIN,1)
    D_FOUT_tmp=np.sum(D_FOUT_tmp,1)
    D_FIN_tmp=np.sum(D_FIN_tmp,1)
    
    output=[D_gst,D_CO2,D_RH,D_NPP,LSNK,D_FIN,D_FOUT,OSNK,
            D_gst_tmp,D_CO2_tmp,D_RH_tmp,D_NPP_tmp,LSNK_tmp,D_FIN_tmp,D_FOUT_tmp,OSNK_tmp]
    writer = csv.writer(open('results_ideal/ideal-'+str(n_run)+'-0.csv','wb'))
    writer.writerows(output)
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))
