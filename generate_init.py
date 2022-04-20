# -*- coding: utf-8 -*-
"""
# Generate common driving data for all subsequent simulations (3000 Monte Carlo 
# simulations). This script should be run first.

@author: Fub
"""

import os

import numpy as np
import xarray as xr

from core_fct.fct_wrap import run_model
from core_fct.fct_loadD import load_all_scen
from core_fct.mod_process import OSCAR
#%%
init_path = './parameters/'
if not os.path.exists(init_path): 
    os.makedirs(init_path)
nMC = 3000  ## Monte Carlo 
var_keep = []
var_keep = ['D_Eluc', 'D_Focean', 'D_Fland', 'D_Epf']
var_keep += ['D_Tg','D_Td','D_Tl','D_To']+['D_Pg','D_Pl']+['D_CO2']
For_rcp = load_all_scen(mod_region='AR6_22reg', group_scen=['RCP2.6', 'RCP4.5', 'RCP6.0', 'RCP8.5'], LCC='gross')
RUN_b = run_model(OSCAR, (1750, 1750, 2014, 2100), For1=For_rcp, mod_region='RCP_5reg', nMC=nMC, output=True, var_keep=var_keep, nt=4)
RUN_b['Par'].to_netcdf(init_path+ 'Par.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['Par']})
RUN_b['For_hist'].to_netcdf(init_path+ 'hist_For.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['For_hist']})
RUN_b['Ini_hist'].to_netcdf(init_path+ 'hist_Ini.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['Ini_hist']})
RUN_b['Out_hist'].to_netcdf(init_path+ 'Out_hist.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['Out_hist']})
RUN_b['For_scen'].to_netcdf(init_path+ 'For_scen.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['For_scen']})
RUN_b['Ini_scen'].to_netcdf(init_path+ 'Ini_scen.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['Ini_scen']})
RUN_b['Out_scen'].to_netcdf(init_path+ 'Out_scen.nc', encoding={var:{'zlib':True, 'dtype':np.float32} for var in RUN_b['Out_scen']})