# -*- coding: utf-8 -*-
"""
# To investigated the effect of different drivers on $CH_4$ lifetime.(Fig.2)

@author: Fub
"""

import os
import numpy as np
import xarray as xr
import time
from core_fct.mod_process import OSCAR

# %%
filepath = './results/lifetime'
if not os.path.exists(filepath):
    os.makedirs(filepath)
# %%
nMC = nMC_hist = nMC_scen = 3000
model = OSCAR
var_keep = []
var_keep += ['D_Tg','D_Td','D_Tl','D_To']+['D_Pg','D_Pl']
var_keep += ['D_CH4','D_Ebb','D_Fsink_CH4']
var_keep += ['tau_CH4']
alpha = 0.01#0.001

# %%

print(model.name + ' loading (historical)')
with xr.open_dataset('parameters/Par.nc') as TMP: Par = TMP.load()
with xr.open_dataset('parameters/hist_Ini.nc') as TMP: Ini_hist = TMP.load()
with xr.open_dataset('parameters/hist_For.nc') as TMP: For_hist = TMP.load()

OSCAR_path = './'
with xr.open_dataset(OSCAR_path+'results/base/base_CH4_hist.nc') as TMP:
    data = TMP.load()
    
D_CO2 = data.D_CO2
D_Tg = data.D_Tg
D_Pg = data.D_Pg
D_Tl = data.D_Tl
D_Pl = data.D_Pl
D_Ebb = data.D_Ebb
D_CH4 = data.D_CH4

# %%
D_CO2_tmp = D_CO2.copy(deep=True)
D_Tg_tmp = D_Tg.copy(deep=True)
D_Pg_tmp = D_Pg.copy(deep=True)
D_Tl_tmp = D_Tl.copy(deep=True)
D_Pl_tmp = D_Pl.copy(deep=True)
D_Ebb_tmp = D_Ebb.copy(deep=True)
D_CH4_tmp = D_CH4.copy(deep=True)

For_hist_clim = xr.merge([For_hist,D_CO2_tmp.mean('config'),D_Tg_tmp.mean('config'),D_Pg_tmp.mean('config'),
                            D_Tl_tmp.mean('config'),D_Pl_tmp.mean('config'),
                            D_Ebb_tmp.mean('config'),
                            D_CH4_tmp.mean('config')])
# %%
filename = 'ABC'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
For_hist_clim_tmp.D_CH4.values *= 0
# E_other
For_hist_clim_tmp.E_NOX.values *= 0
For_hist_clim_tmp.E_VOC.values *= 0
For_hist_clim_tmp.E_CO.values *= 0
For_hist_clim_tmp.D_Ebb.values *= 0
For_hist_clim_tmp.E_Xhalo.values *= 0
# climate
For_hist_clim_tmp.D_CO2.values *= 0
For_hist_clim_tmp.D_Tg.values *= 0
For_hist_clim_tmp.D_Pg.values *= 0
For_hist_clim_tmp.D_Tl.values *= 0
For_hist_clim_tmp.D_Pl.values *= 0
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = 'BC'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
For_hist_clim_tmp.D_CH4.values *= 0
# E_other
# climate
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = 'AC'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
# E_other
For_hist_clim_tmp.E_NOX.values *= 0
For_hist_clim_tmp.E_VOC.values *= 0
For_hist_clim_tmp.E_CO.values *= 0
For_hist_clim_tmp.D_Ebb.values *= 0
For_hist_clim_tmp.E_Xhalo.values *= 0
# climate
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = 'AB'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
# E_other
# climate
For_hist_clim_tmp.D_CO2.values *= 0
For_hist_clim_tmp.D_Tg.values *= 0
For_hist_clim_tmp.D_Pg.values *= 0
For_hist_clim_tmp.D_Tl.values *= 0
For_hist_clim_tmp.D_Pl.values *= 0
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = 'B'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
For_hist_clim_tmp.D_CH4.values *= 0
# E_other
# climate
For_hist_clim_tmp.D_CO2.values *= 0
For_hist_clim_tmp.D_Tg.values *= 0
For_hist_clim_tmp.D_Pg.values *= 0
For_hist_clim_tmp.D_Tl.values *= 0
For_hist_clim_tmp.D_Pl.values *= 0
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = 'A'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
# E_other
For_hist_clim_tmp.E_NOX.values *= 0
For_hist_clim_tmp.E_VOC.values *= 0
For_hist_clim_tmp.E_CO.values *= 0
For_hist_clim_tmp.D_Ebb.values *= 0
For_hist_clim_tmp.E_Xhalo.values *= 0
# climate
For_hist_clim_tmp.D_CO2.values *= 0
For_hist_clim_tmp.D_Tg.values *= 0
For_hist_clim_tmp.D_Pg.values *= 0
For_hist_clim_tmp.D_Tl.values *= 0
For_hist_clim_tmp.D_Pl.values *= 0
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = 'C'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
For_hist_clim_tmp.D_CH4.values *= 0
# E_other
For_hist_clim_tmp.E_NOX.values *= 0
For_hist_clim_tmp.E_VOC.values *= 0
For_hist_clim_tmp.E_CO.values *= 0
For_hist_clim_tmp.D_Ebb.values *= 0
For_hist_clim_tmp.E_Xhalo.values *= 0
# climate
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))
# %%
filename = '0'
print(filename)
For_hist_clim_tmp = For_hist_clim.copy(deep=True)
# D_CH4
# E_other
# climate
Out_hist = model(Ini_hist, Par, For_hist_clim_tmp,var_keep=var_keep)
Out_hist.to_netcdf(filepath+'/'+ filename + '_Out_hist_clim.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in Out_hist})
print(time.asctime( time.localtime(time.time()) ))