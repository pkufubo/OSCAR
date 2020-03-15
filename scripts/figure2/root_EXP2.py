# -*- coding: utf-8 -*-
"""
EXP2 of Fig.2
Attribute D_gst to all drivers
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
fileid='test'
task=0
RF_List=['RF','RF_CO2','RF_CH4','RF_H2Os','RF_N2O','RF_halo',
         'RF_O3t','RF_O3s','RF_SO4','RF_POA','RF_BC','RF_NO3','RF_SOA',
         'RF_cloud','RF_BCsnow','RF_LCC']
[RF,RF_CO2,RF_CH4,RF_H2Os,RF_N2O,RF_halo,
     RF_O3t,RF_O3s,RF_SO4,RF_POA,RF_BC,RF_NO3,RF_SOA,
     RF_cloud,RF_BCsnow,RF_LCC,D_gst,D_gyp]=OSCAR_lite(var_output=RF_List+['D_gst','D_gyp'])
for run_i in range(MC_n):
#    print('No.'+str(run_i+1))
#    print(time.asctime( time.localtime(time.time()) ))
    fileid=str(task)+'-'+str(run_i+1)
    #random configures
    execfile('ran_config.py')
    output_result=[]
    data_RF_IPCC=data_RF_IPCC_orgin
    #attribute
    execfile('init_RF.py')
    [D_gst,D_gyp,RF_CO2,D_CO2,ELUC,LSNK,OSNK]=OSCAR_lite(force_RFs0=True,var_output=['D_gst','D_gyp']+['RF_CO2','D_CO2','ELUC','LSNK','OSNK'])
    ELUC=np.sum(ELUC,1)

    for var in ['CO2','CH4','N2O','O3s','O3t','SO4','LCC','H2Os','BCsnow']:
        #N2O---GHG other;SO4---Aerosol 
        execfile('init_RF.py')
        exec('RF_'+var+'_force=RF_'+var+'_force*(1-alpha)')
        [D_gst_tmp,D_gyp_tmp]=OSCAR_lite(force_RFs0=True,var_output=['D_gst','D_gyp'])
        output_result.append(D_gst[-1]-D_gst_tmp[-1])
    
    execfile('init_RF.py')
    [D_gst_tmp,D_gyp_tmp]=OSCAR_lite(force_RFs0=True,var_output=['D_gst','D_gyp'],RFcon=RFcon.copy()*(1-alpha))
    output_result.append(D_gst[-1]-D_gst_tmp[-1])
    [D_gst_tmp,D_gyp_tmp]=OSCAR_lite(force_RFs0=True,var_output=['D_gst','D_gyp'],RFvolc=RFvolc.copy()*(1-alpha))
    output_result.append(D_gst[-1]-D_gst_tmp[-1])    
    [D_gst_tmp,D_gyp_tmp]=OSCAR_lite(force_RFs0=True,var_output=['D_gst','D_gyp'],RFsolar=RFsolar.copy()*(1-alpha))
    output_result.append(D_gst[-1]-D_gst_tmp[-1])
    
    output_result=output_result/np.sum(output_result)*D_gst[-1]
    #write results
    writer = csv.writer(open('results_exp2/attribution-'+fileid+'.csv','wb'))
    writer.writerow(output_result)
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))   

    #write test_data
    writer = csv.writer(open('results_exp2/weight-'+fileid+'.csv','wb'))
    writer.writerows([D_gst,RF_CO2,D_CO2,ELUC,LSNK,OSNK])
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))
#    print(time.asctime( time.localtime(time.time()) ))
#    print('------')