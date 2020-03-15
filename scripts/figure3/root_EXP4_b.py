# -*- coding: utf-8 -*-
"""
Fig3.b
"""

import csv
import warnings
import time
warnings.filterwarnings("ignore")
execfile('OSCAR.py')
RF_List=['RF','RF_CO2','RF_CH4','RF_H2Os','RF_N2O','RF_halo',
         'RF_O3t','RF_O3s','RF_SO4','RF_POA','RF_BC','RF_NO3','RF_SOA',
         'RF_cloud','RF_BCsnow','RF_LCC']
data_RF_IPCC=np.array([line for line in csv.reader(open('RF_IPCC.csv','r'))],dtype=dty)
alpha=0.01
[RF,RF_CO2,RF_CH4,RF_H2Os,RF_N2O,RF_halo,
 RF_O3t,RF_O3s,RF_SO4,RF_POA,RF_BC,RF_NO3,RF_SOA,
 RF_cloud,RF_BCsnow,RF_LCC,D_gst,D_gyp]=OSCAR_lite(var_output=RF_List+['D_gst','D_gyp'])

MC_n=5
task=0
for run_i in range(MC_n):
    fileid='EXP4-'+str(task)+'-'+str(run_i)
    execfile('ran_config.py')
    execfile('init_RF.py')
    [RF_CO2]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'])
    output_result=[]
    year_0=1700
    #1750:100:1849 (= 1 period)    
    year_start=1750-year_0
    year_end=year_start+100
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    
    #1850:50:1899 (= 1 period)
    year_start=1850-year_0
    year_end=year_start+50
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)    
    #1900:25:1949 (= 2 periods)
    year_start=1900-year_0
    year_end=year_start+25
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)   
    year_start=year_end
    year_end=year_start+25
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)      
    #1950:10:1989 (= 4 periods)
    year_start=1950-year_0
    year_end=year_start+10
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    for i in range (3):
        year_start=year_end
        year_end=year_start+10
        print(time.asctime( time.localtime(time.time()) ))
        print([year_start,year_end])
        execfile('attribute.py')
        output_result.append(temp_output_results)
    #1990:1:1991 (= 2 periods)
    year_start=1990-year_0
    year_end=year_start+1
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    year_start=year_end
    year_end=year_start+1
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    #1992:4:1999 (= 2 periods)
    year_start=1992-year_0
    year_end=year_start+4
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    year_start=year_end
    year_end=year_start+4
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    #2000:2:2009 (= 5 periods)
    year_start=2000-year_0
    year_end=year_start+2
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute.py')
    output_result.append(temp_output_results)
    for i in range (4):
        year_start=year_end
        year_end=year_start+2
        print(time.asctime( time.localtime(time.time()) ))
        print([year_start,year_end])
        execfile('attribute.py')
        output_result.append(temp_output_results)
    #2010
    temp_output_results=[]
    print(time.asctime( time.localtime(time.time()) ))
    print([2010])
    execfile('init_RF.py')
    #EFF
    EFF_tmp=EFF.copy()
    EFF_tmp[-1,:]=[x*(1-alpha) for x in EFF_tmp[-1,:]]
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],EFF=EFF_tmp)
    temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    #LUCs
    LUC_tmp=LUC.copy()
    LUC_tmp[-1,:]=[x*(1-alpha) for x in LUC_tmp[-1,:]]
    SHIFT_tmp=SHIFT.copy()
    SHIFT_tmp[-1,:]=[x*(1-alpha) for x in SHIFT_tmp[-1,:]]
    HARV_tmp=HARV.copy()
    HARV_tmp[-1,:]=[x*(1-alpha) for x in HARV_tmp[-1,:]]
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],LUC=LUC_tmp,SHIFT=SHIFT_tmp,HARV=HARV_tmp)
    temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    #
    #
    for var in ['CH4','N2O','O3s','O3t','SO4','LCC','H2Os','BCsnow']:
        #
        execfile('init_RF.py')
        exec('RF_'+var+'_force=RF_'+var+'_force')      
        exec('RF_'+var+'_force[-1]=RF_'+var+'_force[-1]*(1-alpha)')    
        [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'])
        temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    
     #
    execfile('init_RF.py')
    RFcon_tmp=RFcon.copy()
    RFcon_tmp[year_start:year_end]=[x*(1-alpha) for x in RFcon_tmp[year_start:year_end]]
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],RFcon=RFcon_tmp)
    temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    
    RFvolc_tmp=RFvolc.copy()
    RFvolc_tmp[year_start:year_end]=[x*(1-alpha) for x in RFvolc_tmp[year_start:year_end]]
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],RFvolc=RFvolc_tmp)
    temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    
    RFsolar_tmp=RFsolar.copy()
    RFsolar_tmp[year_start:year_end]=[x*(1-alpha) for x in RFsolar_tmp[year_start:year_end]]
    [RF_CO2_tmp]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'],RFsolar=RFsolar_tmp)
    temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
    output_result.append(temp_output_results)
    
    #write results
    output_result=np.array(output_result)
    writer = csv.writer(open('results_EXP4/'+fileid+'.csv','wb'))
    writer.writerows(output_result)
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))   
