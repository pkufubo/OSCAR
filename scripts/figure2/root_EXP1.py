# -*- coding: utf-8 -*-
"""
EXP1 of Fig.2
Attribute RF_CO2 to EFF,LUCs and the climate
"""

import csv
import warnings
import time
warnings.filterwarnings("ignore")
execfile('OSCAR.py')
data_RF_IPCC_orgin=np.array([line for line in csv.reader(open('RF_IPCC.csv','r'))],dtype=dty)
#Model Carlo run times
MC_n=4000
alpha=0.001
fileid='default-newbaseline'
task=1
RF_List=['RF','RF_CO2','RF_CH4','RF_H2Os','RF_N2O','RF_halo',
         'RF_O3t','RF_O3s','RF_SO4','RF_POA','RF_BC','RF_NO3','RF_SOA',
         'RF_cloud','RF_BCsnow','RF_LCC']
[RF,RF_CO2,RF_CH4,RF_H2Os,RF_N2O,RF_halo,
     RF_O3t,RF_O3s,RF_SO4,RF_POA,RF_BC,RF_NO3,RF_SOA,
     RF_cloud,RF_BCsnow,RF_LCC,D_gst,D_gyp]=OSCAR_lite(var_output=RF_List+['D_gst','D_gyp'])
for run_i in range(MC_n):
    print('No.'+str(run_i+1))
    print(time.asctime( time.localtime(time.time()) ))
    fileid=str(task)+'-'+str(run_i+1)
    
    execfile('ran_config.py')
    
    output_result=[]
    data_RF_IPCC=data_RF_IPCC_orgin
    execfile('init_RF.py')
    [D_gst_RFs,D_sst_RFs,D_lst_RFs,D_lyp_RFs]=OSCAR_lite(force_RFs=True,var_output=['D_gst','D_sst','D_lst','D_lyp'])    
    
    #attribute
    D_gst_force=D_gst_RFs.copy()
    D_sst_force=D_sst_RFs.copy()
    D_lst_force=D_lst_RFs.copy()
    D_lyp_force=D_lyp_RFs.copy()
    
    [D_CO2,RF_CO2,ELUC,LSNK,OSNK,D_gst]= OSCAR_lite(force_RFs=True,force_clim=True,var_output=['D_CO2','RF_CO2','ELUC','LSNK','OSNK']+['D_gst'])
    ELUC=np.sum(ELUC,1)
    [D_CO2_EFF,RF_CO2_EFF]= OSCAR_lite(force_RFs=True,force_clim=True,var_output=['D_CO2','RF_CO2'],EFF=EFF.copy()*(1-alpha))
    [D_CO2_luc,RF_CO2_luc]= OSCAR_lite(force_RFs=True,force_clim=True,var_output=['D_CO2','RF_CO2'],LUC=LUC.copy()*(1-alpha),SHIFT=SHIFT.copy()*(1-alpha),HARV=HARV.copy()*(1-alpha))

    D_gst_force=D_gst_RFs*(1-alpha)
    D_sst_force=D_sst_RFs*(1-alpha)
    D_lst_force=D_lst_RFs*(1-alpha)
    D_lyp_force=D_lyp_RFs*(1-alpha)
    [D_CO2_gst,RF_CO2_gst]= OSCAR_lite(force_RFs=True,force_clim=True,var_output=['D_CO2','RF_CO2'])
    #attribute
    att_D_CO2_EFF=(D_CO2[-1]-D_CO2_EFF[-1])/(3*D_CO2[-1]-D_CO2_EFF[-1]-D_CO2_luc[-1]-D_CO2_gst[-1])*D_CO2[-1]
    att_D_CO2_luc=(D_CO2[-1]-D_CO2_luc[-1])/(3*D_CO2[-1]-D_CO2_EFF[-1]-D_CO2_luc[-1]-D_CO2_gst[-1])*D_CO2[-1]
    att_D_CO2_gst=(D_CO2[-1]-D_CO2_gst[-1])/(3*D_CO2[-1]-D_CO2_EFF[-1]-D_CO2_luc[-1]-D_CO2_gst[-1])*D_CO2[-1]
    att_RF_CO2_EFF=(RF_CO2[-1]-RF_CO2_EFF[-1])/(3*RF_CO2[-1]-RF_CO2_EFF[-1]-RF_CO2_luc[-1]-RF_CO2_gst[-1])*RF_CO2[-1]
    att_RF_CO2_luc=(RF_CO2[-1]-RF_CO2_luc[-1])/(3*RF_CO2[-1]-RF_CO2_EFF[-1]-RF_CO2_luc[-1]-RF_CO2_gst[-1])*RF_CO2[-1]
    att_RF_CO2_gst=(RF_CO2[-1]-RF_CO2_gst[-1])/(3*RF_CO2[-1]-RF_CO2_EFF[-1]-RF_CO2_luc[-1]-RF_CO2_gst[-1])*RF_CO2[-1]  
    #write results
    writer = csv.writer(open('results_EXP1/attribution-'+fileid+'.csv','wb'))
    writer.writerow([att_D_CO2_EFF,att_D_CO2_luc,att_D_CO2_gst])
    writer.writerow([att_RF_CO2_EFF,att_RF_CO2_luc,att_RF_CO2_gst])
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))

    #write test_data
    writer = csv.writer(open('results_EXP1/weight-'+fileid+'.csv','wb'))
    writer.writerows([D_gst,RF_CO2,D_CO2,ELUC,LSNK,OSNK])
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))
    print(time.asctime( time.localtime(time.time()) ))
    print('------')