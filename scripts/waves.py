# coding: utf-8

from glob import glob
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
'''
ds = xr.open_mfdataset(sorted(glob('/glade/scratch/mcamron/archive/f.c54120.FWscHIST.f09_f09.gwdst/atm/hist/f.c54120.FWscHIST.f09_f09.gwdst.cam.h1.2002-0[6,7]*')))

ds = ds.sel(lat=slice(-20,20))

# Separate out GW flux vars and convert Pa -> mPa
gwx = xr.Dataset({var: ds[var] for var in ds.data_vars if 'BTAUX' in var}) * 1000
gwy = xr.Dataset({var: ds[var] for var in ds.data_vars if 'BTAUY' in var}) * 1000

tau = xr.Dataset({str(i): xu.sqrt(xu.square(gwx[x]) + xu.square(gwy[y])) for (i, (x,y)) in enumerate(zip(gwx.data_vars, gwy.data_vars))})

tau.to_netcdf('/glade/scratch/mcamron/output/gwdst/tau_magnitude.nc')
'''

tau = xr.open_dataset('/glade/scratch/mcamron/output/gwdst/tau_magnitude.nc', chunks={'time': 61})

bins = np.arange(0, 200, 1)
hist = 0

for (i, x) in enumerate(tau.data_vars):
    (h, edges) = np.histogram(tau[str(i)], bins=bins)
    hist += h

tau_hist = xr.DataArray(hist, coords={'edges': edges}, dims='bins')
tau_hist.to_netcdf('/glade/scratch/mcamron/output/gwdst/tau_hist.nc')

f, ax = plt.subplots(figsize=(7, 6))
ax.step(edges[:-1], hist, where='post', linewidth=2)
ax.semilogy()
ax.set_xlim(0, 200)

ax.set_title('Beres tau parameterized convective GW flux (All waves)')
ax.set_xlabel('Flux [mPa]')

plt.tight_layout()

f.savefig('~/python/gwdst/figures/waves/dist_flux.png')
