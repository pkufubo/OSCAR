# -*- coding: utf-8 -*-
"""
# Run base simulation of methane, including history and RCP.

@author: Fub
"""


import os
import numpy as np
import xarray as xr
from core_fct.mod_process import OSCAR
# %%

filepath = './results/base'
if not os.path.exists(filepath): 
    os.makedirs(filepath)
model = OSCAR
inds = (1750, 1750, 2014)
mod_region = 'AR6_22reg'

var_keep = []
var_keep = ['D_Eluc', 'D_Focean', 'D_Fland', 'D_Epf'] + [var for var in list(OSCAR._processes.keys()) if 'RF' in var]
var_keep += ['D_Tg','D_Td','D_Tl','D_To']+['D_Pg','D_Pl']
var_keep += ['RF_CH4'] 
var_keep += ['D_CH4', 'E_CH4', 'D_Ewet', 'D_Ebb', 'D_Epf_CH4', 'D_Fsink_CH4']
var_keep += ['D_CO2','D_N2O']+['D_CH4_lag']
var_keep += ['D_Foh_CH4', 'D_Fhv_CH4', 'D_Fsoil_CH4', 'D_Focean_CH4']
var_keep += ['tau_CH4']

# %%
########################################
# Read in parameters
########################################
with xr.open_dataset('parameters/Par.nc') as TMP: Par = TMP.load()
with xr.open_dataset('parameters/hist_Ini.nc') as TMP: Ini_hist = TMP.load()
with xr.open_dataset('parameters/hist_For.nc') as TMP: For_hist = TMP.load()
with xr.open_dataset('parameters/For_scen.nc') as TMP: For_scen = TMP.load()
with xr.open_dataset('parameters/Ini_scen.nc') as TMP: Ini_scen = TMP.load()
# %%
filename = 'base_CH4_hist'
Out_hist = model(Ini_hist, Par, For_hist,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
# %%
filename = 'base_CH4_future'
Out_scen = model(Ini_scen, Par, For_scen,var_keep=var_keep)
Out_scen.to_netcdf(filepath+'/'+ filename + '.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_scen})
