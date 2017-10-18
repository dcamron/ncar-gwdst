# coding: utf-8

#from glob import glob
import numpy as np
import pandas as pd
import xarray as xr
#import xarray.ufuncs as xu
#import matplotlib as mpl
#mpl.use('Agg')
#import matplotlib.pyplot as plt
#import seaborn as sns

#sns.set(context='talk', palette='colorblind', style='ticks')

#####
tau = xr.open_dataset('/glade/scratch/mcamron/output/gwdst/tau_magnitude.nc') #, chunks={'time': 61})

tau_f = xr.concat([tau[i] for i in tau.data_vars], pd.Index(np.arange(1,65), name='wave'))
tau_f.to_netcdf('/glade/scratch/mcamron/output/gwdst/tau_magnitude_f.nc')

'''
f, ax = plt.subplots(figsize=(7, 6))
ax.step(edges[:-1], hist, where='post', linewidth=2)
ax.semilogy()
ax.set_xlim(0, 200)

ax.set_title('Beres tau parameterized convective GW flux (All waves)')
ax.set_xlabel('Flux [mPa]')

plt.tight_layout()

f.savefig('~/python/gwdst/figures/waves/dist_flux.png')
'''
