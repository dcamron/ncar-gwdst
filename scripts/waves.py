# coding: utf-8

import numpy as np
import pandas as pd
import xarray as xr
import xarray.ufuncs as xu
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(context='talk', palette='colorblind', style='ticks')

#####

ds = xr.open_mfdataset('/glade/scratch/mcamron/archive/f.c54120.FWscHIST.f09_f09.gwdst/atm/hist/f.c54120.FWscHIST.f09_f09.gwdst.cam.h1.2002-07-*.nc')

ds = ds.sel(lat=slice(-20,20))

# Separate out GW flux vars and convert Pa -> mPa
gwx = xr.Dataset({var: ds[var] for var in ds.data_vars if 'BTAUX' in var}) * 1000
gwy = xr.Dataset({var: ds[var] for var in ds.data_vars if 'BTAUY' in var}) * 1000

tau = xr.Dataset({str(i): xu.sqrt(xu.square(gwx[x]) + xu.square(gwy[y])) for (i, (x,y)) in enumerate(zip(gwx.data_vars, gwy.data_vars))})

tau.to_netcdf('/glade/scratch/mcamron/output/gwdst/tau_magnitude.nc')

tau = xr.open_dataset('/glade/scratch/mcamron/output/gwdst/tau_magnitude.nc', chunks={'time': 31})

mx = 0
for (i, x) in enumerate(tau.data_vars):
    if tau[i].max().values > mx:
        mx = tau[i].max().values

bins = np.arange(0, 200, 1)
hist = 0

for (i, x) in enumerate(tau.data_vars):
    (h, edges) = np.histogram(tau[i], bins=bins)
    hist += h

f, ax = plt.subplots(figsize=(7, 6))
ax.step(edges[:-1], hist, where='post', linewidth=2)
ax.semilogy()
ax.set_xlim(0, 200)

ax.set_title('Beres tau parameterized convective GW flux (All waves)')
ax.set_xlabel('Flux [mPa]')

plt.tight_layout()

f.savefig('../figures/waves/dist_flux.png')
