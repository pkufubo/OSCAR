# -*- coding: utf-8 -*-
"""
Attribute RF_CO2 and D_CO2 to EFF,LUCs and climate
Step1 in Fig2
"""

import csv
import warnings
import time
warnings.filterwarnings("ignore")
execfile('OSCAR.py')
data_RF_IPCC_orgin=np.array([line for line in csv.reader(open('RF_IPCC.csv','r'))],dtype=dty)[1:-1]
#Model Carlo run times
MC_n=4000
alpha=0.001
fileid='default-newbaseline'
task=0
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
    #execfile('ran_config.py')
    output_result=[]
    IPCC_RF_uncertainty=[0.1,0.1025,0.5,2,1.278,0.667,0.714,0.875,1.25,1,1]
    data_RF_IPCC=[]
    for i in range(len(IPCC_RF_uncertainty)):
        data_RF_IPCC.append(np.random.normal(0,IPCC_RF_uncertainty[i]/1.96,len(data_RF_IPCC_orgin)))
    data_RF_IPCC=np.array(data_RF_IPCC)
    data_RF_IPCC=data_RF_IPCC.T
    data_RF_IPCC=data_RF_IPCC*data_RF_IPCC_orgin+data_RF_IPCC_orgin
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
    writer = csv.writer(open('results_EXP1/#OUT.USELESS.empty','wb'))
    
    #Save configures
    configure_list=[]
    for var in [data_EFF,data_LULCC,data_ECH4,data_EN2O,data_Ehalo,
        data_ENOX,data_ECO,data_EVOC,data_ESO2,data_ENH3,data_EOC,data_EBC,data_RFant,data_RFnat]:
        configure_list.append([var])
    for var in [mod_OSNKstruct,mod_OSNKchem,mod_OSNKtrans,mod_LSNKnpp,mod_LSNKrho,mod_LSNKpreind,mod_LSNKtrans,mod_LSNKcover,
        mod_EFIREpreind,mod_EFIREtrans,mod_ELUCagb,mod_EHWPbb,mod_EHWPtau,mod_EHWPfct,
        mod_OHSNKtau,mod_OHSNKfct,mod_OHSNKtrans,mod_EWETpreind,mod_AWETtrans,mod_HVSNKtau,mod_HVSNKtrans,mod_HVSNKcirc,
        mod_O3Tregsat,mod_O3Temis,mod_O3Tclim,mod_O3Tradeff,mod_O3Sfracrel,mod_O3Strans,mod_O3Snitrous,mod_O3Sradeff,
        mod_SO4regsat,mod_SO4load,mod_SO4radeff,mod_POAconv,mod_POAregsat,mod_POAload,mod_POAradeff,
        mod_BCregsat,mod_BCload,mod_BCradeff,mod_BCadjust,mod_NO3load,mod_NO3radeff,mod_SOAload,mod_SOAradeff,
        mod_DUSTload,mod_DUSTradeff,mod_SALTload,mod_SALTradeff,mod_CLOUDsolub,mod_CLOUDerf,mod_CLOUDpreind,
        mod_ALBBCreg,mod_ALBBCrf,mod_ALBBCwarm,mod_ALBLCflux,mod_ALBLCalb,mod_ALBLCcover,mod_ALBLCwarm,
        mod_TEMPresp,mod_TEMPpattern,mod_PRECresp,mod_PRECradfact,mod_PRECpattern,mod_ACIDsurf,mod_SLR]:
        configure_list.append([var])
    
    writer = csv.writer(open('results_EXP1/configure-'+fileid+'.csv','wb'))
    writer.writerows(configure_list)
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))
                             
    #write test_data
    writer = csv.writer(open('results_EXP1/weight-'+fileid+'.csv','wb'))
    writer.writerows([D_gst,RF_CO2,D_CO2,ELUC,LSNK,OSNK])
    writer = csv.writer(open('results/#OUT.USELESS.empty','wb'))
    print(time.asctime( time.localtime(time.time()) ))
    print('------')
