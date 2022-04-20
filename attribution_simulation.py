# -*- coding: utf-8 -*-
"""
# To attribute the increases in $CH_4$ atmospheric concentrations to anthropogenic
# emission of $CH_4$, reactive species, and climate feedbacks.(Fig.3)
@author: Fub
"""

import os
import numpy as np
import xarray as xr
import time

from core_fct.mod_process import OSCAR

# %%
filepath = './results/attribution1.0'
if not os.path.exists(filepath):
    os.makedirs(filepath)

# %%

nMC = nMC_hist = nMC_scen = 3000
model = OSCAR
LCC = 'gross'
inds = (1750, 1750, 2014)
mod_region = 'RCP_5reg'
var_keep = []

var_keep = ['D_Eluc', 'D_Focean', 'D_Fland', 'D_Epf'] + [var for var in list(OSCAR._processes.keys()) if 'RF' in var]
var_keep += ['D_Tg','D_Td','D_Tl','D_To']+['D_Pg','D_Pl']
var_keep += ['RF_CH4'] 
var_keep += ['D_CH4', 'E_CH4', 'D_Ewet', 'D_Ebb', 'D_Epf_CH4', 'D_Fsink_CH4']
var_keep += ['D_CO2','D_N2O']+['D_CH4_lag']
var_keep += ['D_Foh_CH4', 'D_Fhv_CH4', 'D_Fsoil_CH4', 'D_Focean_CH4']
var_keep += ['tau_CH4']
alpha = 0.01#0.001

# %%
print(model.name + ' loading (historical)')
with xr.open_dataset('parameters/Par.nc') as TMP: Par = TMP.load()
with xr.open_dataset('parameters/hist_Ini.nc') as TMP: Ini_hist = TMP.load()
with xr.open_dataset('parameters/hist_For.nc') as TMP: For_hist = TMP.load()

# %%

OSCAR_path = './'
with xr.open_dataset(OSCAR_path+'results/base/base_CH4_hist.nc') as TMP:
    data = TMP.load()
D_CO2 = data.D_CO2
D_Tg = data.D_Tg
D_Pg = data.D_Pg
D_Tl = data.D_Tl
D_Pl = data.D_Pl
D_Ebb = data.D_Ebb

# %%
D_CO2_tmp = D_CO2.copy(deep=True)
D_Tg_tmp = D_Tg.copy(deep=True)
D_Pg_tmp = D_Pg.copy(deep=True)
D_Tl_tmp = D_Tl.copy(deep=True)
D_Pl_tmp = D_Pl.copy(deep=True)
D_Ebb_tmp = D_Ebb.copy(deep=True)
For_hist_clim = xr.merge([For_hist,D_CO2_tmp.mean('config'),D_Tg_tmp.mean('config'),D_Pg_tmp.mean('config'),
                            D_Tl_tmp.mean('config'),D_Pl_tmp.mean('config'),
                            D_Ebb_tmp.mean('config')])

# %%

print(time.asctime( time.localtime(time.time()) ))
Out_hist = model(Ini_hist, Par, For_hist_clim,var_keep=var_keep)
filename = 'base'
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%

driver_list = ['E_CH4','E_N2O']+['E_CO','E_VOC','E_NOX','E_Xhalo']+['clim']
positive_lit = [0,2,3]
positive_lit = []
# for driver in ['Eff']:
for driver in driver_list:
    
    if driver in ['E_CH4','clim']:
        continue
    filename = driver
    print(filename)
    print(time.asctime( time.localtime(time.time()) ))
    For_hist_tmp = For_hist_clim.copy(deep=True)
    # if driver_list.index(driver) in positive_lit:
    #     For_hist_tmp[driver].values[:] *= (1-alpha)
    # else:
    #     For_hist_tmp[driver].values[:] *= (1+alpha)
    For_hist_tmp[driver].values[:] *= (1-alpha)
    Out_hist_clim = model(Ini_hist, Par, For_hist_tmp,var_keep=var_keep)
    Out_hist_clim.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
    print(time.asctime( time.localtime(time.time()) ))



# %%
filename = 'clim'
print(filename)
print(time.asctime( time.localtime(time.time()) ))
For_hist_tmp = For_hist_clim.copy(deep=True)
For_hist_tmp['D_CO2'].values[:] *= (1-alpha)
For_hist_tmp['D_Tg'].values[:] *= (1-alpha)
For_hist_tmp['D_Pg'].values[:] *= (1-alpha)
For_hist_tmp['D_Tl'].values[:] *= (1-alpha)
For_hist_tmp['D_Pl'].values[:] *= (1-alpha)
Out_hist_clim = model(Ini_hist, Par, For_hist_tmp,var_keep=var_keep)
Out_hist_clim.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))

filename = 'E_CH4'
print(filename)
print(time.asctime( time.localtime(time.time()) ))
For_hist_tmp = For_hist_clim.copy(deep=True)
For_hist_tmp['E_CH4'].values[:] *= (1-alpha)
For_hist_tmp.D_Ebb.sel(spc_bb='CH4').values[:] *= (1-alpha)
Out_hist_clim = model(Ini_hist, Par, For_hist_tmp,var_keep=var_keep)
Out_hist_clim.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist_clim})
print(time.asctime( time.localtime(time.time()) ))

# %%

filename = 'clim_sinkonly'
print(filename)
print(time.asctime( time.localtime(time.time()) ))
For_hist_tmp = For_hist_clim.copy(deep=True)
For_hist_tmp['D_CO2'].values[:] *= (1-alpha)
For_hist_tmp['D_Tg'].values[:] *= (1-alpha)
For_hist_tmp['D_Pg'].values[:] *= (1-alpha)
For_hist_tmp['D_Tl'].values[:] *= (1-alpha)
For_hist_tmp['D_Pl'].values[:] *= (1-alpha)

For_hist_tmp =  xr.merge([For_hist_tmp,
                          Out_hist.D_Ewet,Out_hist.D_Epf_CH4])

Out_hist_clim = model(Ini_hist, Par, For_hist_tmp,var_keep=var_keep)
Out_hist_clim.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))

# %%
filename = 'clim_emissonly'
print(filename)
print(time.asctime( time.localtime(time.time()) ))
For_hist_tmp = For_hist_clim.copy(deep=True)
For_hist_tmp['D_CO2'].values[:] *= (1-alpha)
For_hist_tmp['D_Tg'].values[:] *= (1-alpha)
For_hist_tmp['D_Pg'].values[:] *= (1-alpha)
For_hist_tmp['D_Tl'].values[:] *= (1-alpha)
For_hist_tmp['D_Pl'].values[:] *= (1-alpha)

For_hist_tmp =  xr.merge([For_hist_tmp,
                          Out_hist.D_Fsink_CH4])

Out_hist_clim = model(Ini_hist, Par, For_hist_tmp,var_keep=var_keep)
Out_hist_clim.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
