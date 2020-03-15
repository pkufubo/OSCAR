# -*- coding: utf-8 -*-
"""
Read in IPCC RF data
"""

TMP=data_RF_IPCC
#
RF_CO2_force=RF_CO2.copy()
RF_CO2_force[-260:]=TMP[:,0]
RF_O3t_force=RF_O3t.copy()
RF_O3t_force[-260:]=TMP[:,2]
RF_O3s_force=RF_O3s.copy()
RF_O3s_force[-260:]=TMP[:,3]
RF_LCC_force=RF_LCC.copy()
RF_LCC_force[-260:]=TMP[:,5]
RF_H2Os_force=RF_H2Os.copy()
RF_H2Os_force[-260:]=TMP[:,6]
RF_BCsnow_force=RF_BCsnow.copy()
RF_BCsnow_force[-260:]=TMP[:,7]
#
RF_CH4_force=RF_CH4.copy()#GH Other*
RF_CH4_force[-260:]=TMP[:,1]
RF_N2O_force=RF_N2O.copy()*0
RF_halo_force=RF_halo.copy()*0

RF_SO4_force=RF_SO4.copy() #IPCC provide Aerosol(Total)
RF_NO3_force=RF_NO3.copy()*0
RF_BC_force=RF_BC.copy()*0
RF_POA_force=RF_POA.copy()*0
RF_SOA_force=RF_SOA.copy()*0
RF_SOA_force=RF_SOA.copy()*0
RF_cloud=RF_cloud.copy()*0
#
RFcon[-260:]=TMP[:,-3]
RFsolar[-260:]=TMP[:,-2]
RFvolc[-260:]=TMP[:,-1]
