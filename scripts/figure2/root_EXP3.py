# -*- coding: utf-8 -*-
"""
EXP3 of Fig.2
Attribute RF_CO2 to all drivers
"""
import csv
import warnings
import time
warnings.filterwarnings("ignore")
execfile('OSCAR.py')
#直接按照IPCC的来分配
data_RF_IPCC_orgin=np.array([line for line in csv.reader(open('RF_IPCC.csv','r'))],dtype=dty)
#Model Carlo run times
MC_n=4000
alpha=0.001
fileid='test'
task=4
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
    #random configures
    execfile('ran_config.py')
    output_result=[]
    data_RF_IPCC=data_RF_IPCC_orgin
    #attribute
    execfile('init_RF.py')
    #[RF_CO2]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'])
    [D_CO2,RF_CO2,ELUC,LSNK,OSNK,D_gst]= OSCAR_lite(force_RFs=True,var_output=['D_CO2','RF_CO2','ELUC','LSNK','OSNK','D_gst'])
    ELUC=np.sum(ELUC,1)
    #二氧化碳、LUC
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],EFF=EFF.copy()*(1-alpha))
    output_result.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],LUC=LUC.copy()*(1-alpha),SHIFT=SHIFT.copy()*(1-alpha),HARV=HARV.copy()*(1-alpha))
    output_result.append(RF_CO2[-1]-RF_CO2_tmp[-1])
      
    #其他温室气体、对流层臭氧、平流层臭氧、气溶胶、土地反照度、平流层水汽、雪表黑炭、航迹云、太阳活动、火山活动
    for var in ['CH4','N2O','O3s','O3t','SO4','LCC','H2Os','BCsnow']: #这里O3S和O3t的顺序反了
        #CH4---GHG other;SO4---Aerosol 
        execfile('init_RF.py')
        exec('RF_'+var+'_force=RF_'+var+'_force*(1-alpha)')
        [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'])
        output_result.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    
    execfile('init_RF.py')
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],RFcon=RFcon.copy()*(1-alpha))
    output_result.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],RFvolc=RFvolc.copy()*(1-alpha))
    output_result.append(RF_CO2[-1]-RF_CO2_tmp[-1])    
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],RFsolar=RFsolar.copy()*(1-alpha))
    output_result.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    
    output_result=output_result/np.sum(output_result)*RF_CO2[-1]
    #write results
    writer = csv.writer(open('results_EXP3/attribution-'+fileid+'.csv','wb'))
    writer.writerow(output_result)
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))   
                         
    #write test_data
    writer = csv.writer(open('results_EXP3/weight-'+fileid+'.csv','wb'))
    writer.writerows([D_gst,RF_CO2,D_CO2,ELUC,LSNK,OSNK])
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))
    print(time.asctime( time.localtime(time.time()) ))
    print('------')
                             
