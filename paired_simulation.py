# -*- coding: utf-8 -*-
"""
# To demonstrate the effect of climate feedbacks on atmospheric $CH_4$ 
concentrations.(Fig.1)

@author: Fub
"""
## %%

import os

import numpy as np
import xarray as xr
import time 

from core_fct.mod_process import OSCAR
#%%
init_path = './parameters/'
if not os.path.exists(init_path): 
    os.makedirs(init_path)

nMC = 3000

model = OSCAR
var_keep = []
var_keep = ['D_Eluc', 'D_Focean', 'D_Fland', 'D_Epf'] + [var for var in list(OSCAR._processes.keys()) if 'RF' in var]
var_keep += ['D_Tg','D_Td','D_Tl','D_To']+['D_Pg','D_Pl']

var_keep += ['RF_CH4'] 
var_keep += ['D_CH4', 'E_CH4', 'D_Ewet', 'D_Ebb', 'D_Epf_CH4', 'D_Fsink_CH4']
var_keep += ['D_CO2','D_N2O']+['D_CH4_lag']+['tau_CH4']
var_keep += ['D_Foh_CH4', 'D_Fhv_CH4', 'D_Fsoil_CH4', 'D_Focean_CH4']
# %%
with xr.open_dataset('parameters/Par.nc') as TMP: Par = TMP.load()
with xr.open_dataset('parameters/hist_Ini.nc') as TMP: Ini_hist = TMP.load()
with xr.open_dataset('parameters/hist_For.nc') as TMP: For_hist = TMP.load()
with xr.open_dataset('parameters/For_scen.nc') as TMP: For_scen = TMP.load()
with xr.open_dataset('parameters/Ini_scen.nc') as TMP: Ini_scen = TMP.load()

# %%
OSCAR_path = 'F:/OSCAR/'
with xr.open_dataset(OSCAR_path+'results/base/base_CH4_hist.nc') as TMP:
    data = TMP.load()

D_CO2_hist = data.D_CO2.copy(deep=True)
D_Tg_hist = data.D_Tg.copy(deep=True)
D_Pg_hist = data.D_Pg.copy(deep=True)
D_Tl_hist = data.D_Tl.copy(deep=True)
D_Pl_hist = data.D_Pl.copy(deep=True)
D_Ebb_hist = data.D_Ebb.copy(deep=True)

For_hist_normal = xr.merge([For_hist,
                            D_CO2_hist.mean('config'),
                            D_Tg_hist.mean('config'),D_Pg_hist.mean('config'),
                            D_Tl_hist.mean('config'),D_Pl_hist.mean('config'),
                            D_Ebb_hist.mean('config')])

# %%
with xr.open_dataset(OSCAR_path+'results/base/base_CH4_future.nc') as TMP:
    data = TMP.load()
D_CO2_scen = data.D_CO2.copy(deep=True)
D_Tg_scen = data.D_Tg.copy(deep=True)
D_Pg_scen = data.D_Pg.copy(deep=True)
D_Tl_scen = data.D_Tl.copy(deep=True)
D_Pl_scen = data.D_Pl.copy(deep=True)
D_Ebb_scen = data.D_Ebb.copy(deep=True)

For_scen_normal = xr.merge([For_scen,
                            D_CO2_scen.mean('config'),
                            D_Tg_scen.mean('config'),D_Pg_scen.mean('config'),
                            D_Tl_scen.mean('config'),D_Pl_scen.mean('config'),
                            D_Ebb_scen.mean('config')])

# %%
filepath = './results/future'
if not os.path.exists(filepath):
    os.makedirs(filepath)


print(time.asctime( time.localtime(time.time()) ))
filename = 'T_hist'
Out_hist_normal = model(Ini_hist, Par, For_hist_normal,var_keep=var_keep)
Out_hist_normal.to_netcdf(filepath+'/'+ filename + '.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist_normal})
print(time.asctime( time.localtime(time.time()) ))

Ini_scen = Out_hist_normal.isel(year=-1, drop=True).drop([VAR for VAR in Out_hist_normal if VAR not in list(model.var_prog)])
filename = 'T_scen'
Ini_scen_normal = Out_hist_normal.isel(year=-1, drop=True).drop([VAR for VAR in Out_hist_normal if VAR not in list(model.var_prog)])
Out_scen_normal = model(Ini_scen, Par, For_scen_normal,var_keep=var_keep)
Out_scen_normal.to_netcdf(filepath+'/'+ filename + '.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_scen_normal})
print(time.asctime( time.localtime(time.time()) ))
# %%%%%
#######
#######
#######
D_CO2_tmp = D_CO2_hist.copy(deep=True)
D_CO2_tmp.sel(year=slice(1850,2014)).values[:] = D_CO2_hist.sel(year=1850).values


D_Tg_tmp = D_Tg_hist.copy(deep=True)
D_Tg_tmp.sel(year=slice(1850,2014)).values[:] = D_Tg_hist.sel(year=1850).values

D_Pg_tmp = D_Pg_hist.copy(deep=True)
D_Pg_tmp.sel(year=slice(1850,2014)).values[:] = D_Pg_hist.sel(year=1850).values

D_Tl_tmp = D_Tl_hist.copy(deep=True)
D_Tl_tmp.sel(year=slice(1850,2014)).values[:] = D_Tl_hist.sel(year=1850).values

D_Pl_tmp = D_Pl_hist.copy(deep=True)
D_Pl_tmp.sel(year=slice(1850,2014)).values[:] = D_Pl_hist.sel(year=1850).values
    
For_hist_Lower = xr.merge([For_hist,D_CO2_tmp.mean('config'),
                           D_Tg_tmp.mean('config'),D_Pg_tmp.mean('config'),
                           D_Tl_tmp.mean('config'),D_Pl_tmp.mean('config'),
                           D_Ebb_hist.mean('config')])

# %%
filename = 'No_T_hist'
Out_hist_Lower = model(Ini_hist, Par, For_hist_Lower,var_keep=var_keep)
Out_hist_Lower.to_netcdf(filepath+'/'+ filename + '.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist_Lower})
print(time.asctime( time.localtime(time.time()) ))
# %%
###############
D_CO2_tmp = D_CO2_scen.copy(deep=True)
D_Tg_tmp = D_Tg_scen.copy(deep=True)
D_Pg_tmp = D_Pg_scen.copy(deep=True)
D_Tl_tmp = D_Tl_scen.copy(deep=True)
D_Pl_tmp = D_Pl_scen.copy(deep=True)
D_Ebb_tmp = D_Ebb_scen.copy(deep=True)
for i in range(4):
    D_CO2_tmp.sel(year=slice(2014,2100)).isel(scen=i).values[:] = D_CO2_hist.sel(year=1850).values
    D_Tg_tmp.sel(year=slice(2014,2100)).isel(scen=i).values[:] = D_Tg_hist.sel(year=1850).values
    D_Pg_tmp.sel(year=slice(2014,2100)).isel(scen=i).values[:] = D_Pg_hist.sel(year=1850).values
    D_Tl_tmp.sel(year=slice(2014,2100)).isel(scen=i).values[:] = D_Tl_hist.sel(year=1850).values
    D_Pl_tmp.sel(year=slice(2014,2100)).isel(scen=i).values[:] = D_Pl_hist.sel(year=1850).values

For_scen_Lower = xr.merge([For_scen,D_CO2_tmp.mean('config'),
                           D_Tg_tmp.mean('config'),D_Pg_tmp.mean('config'),
                           D_Tl_tmp.mean('config'),D_Pl_tmp.mean('config'),
                           D_Ebb_tmp.mean('config')])
# %%
filename = 'No_T_scen'
Ini_scen_Lower = Out_hist_Lower.isel(year=-1, drop=True).drop([VAR for VAR in Out_hist_Lower if VAR not in list(model.var_prog)])
Out_scen_Lower = model(Ini_scen_Lower, Par, For_scen_Lower,var_keep=var_keep)
Out_scen_Lower.to_netcdf(filepath+'/'+ filename + '.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_scen_Lower})
print(time.asctime( time.localtime(time.time()) ))
