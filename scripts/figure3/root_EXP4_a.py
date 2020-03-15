# -*- coding: utf-8 -*-
"""
Fig3.a
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
execfile('init_RF.py')
[RF_CO2]=OSCAR_lite(force_RFs=True,var_output=['RF_CO2'])
[D_gst_RFs,D_sst_RFs,D_lst_RFs,D_lyp_RFs]=OSCAR_lite(force_RFs=True,var_output=['D_gst','D_sst','D_lst','D_lyp'])    
execfile('init_clim.py')

output_result=[]
year_0=1700
#1750:100:1849 (= 1 period)    
year_start=1750-year_0
year_end=year_start+100
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)

#1850:50:1899 (= 1 period)
year_start=1850-year_0
year_end=year_start+50
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)    
#1900:25:1949 (= 2 periods)
year_start=1900-year_0
year_end=year_start+25
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)   
year_start=year_end
year_end=year_start+25
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)      
#1950:10:1989 (= 4 periods)
year_start=1950-year_0
year_end=year_start+10
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)
for i in range (3):
    year_start=year_end
    year_end=year_start+10
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute-clim.py')
    output_result.append(temp_output_results)
#1990:1:1991 (= 2 periods)
year_start=1990-year_0
year_end=year_start+1
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)
year_start=year_end
year_end=year_start+1
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)
#1992:4:1999 (= 2 periods)
year_start=1992-year_0
year_end=year_start+4
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)
year_start=year_end
year_end=year_start+4
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)
#2000:2:2009 (= 5 periods)
year_start=2000-year_0
year_end=year_start+2
print(time.asctime( time.localtime(time.time()) ))
print([year_start,year_end])
execfile('attribute-clim.py')
output_result.append(temp_output_results)
for i in range (4):
    year_start=year_end
    year_end=year_start+2
    print(time.asctime( time.localtime(time.time()) ))
    print([year_start,year_end])
    execfile('attribute-clim.py')
    output_result.append(temp_output_results)
#2010
temp_output_results=[]
print(time.asctime( time.localtime(time.time()) ))
print([2010])
execfile('init_clim.py')
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
#climate
D_gst_force[-1]*=(1-alpha)
D_sst_force[-1]*=(1-alpha)
D_lst_force[-1]*=(1-alpha)
D_lyp_force[-1]*=(1-alpha)
[RF_CO2_tmp]=OSCAR_lite(force_RFs=True,force_clim=True,var_output=['RF_CO2'])
temp_output_results.append(RF_CO2[-1]-RF_CO2_tmp[-1])
output_result.append(temp_output_results)										 

#write results
output_result=np.array(output_result)
writer = csv.writer(open('results_EXP4/EXP4-clim.csv','wb'))
writer.writerows(output_result)
writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))   
