# pip install netCDF4
# pip install numpy --upgrade
# pip install proj
# pip install https://github.com/matplotlib/basemap/archive/master.zip

from netCDF4 import Dataset
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

nc_file = 'pr_mClimMean_PRISM_historical_19810101-20101231.nc.nc'
fh = Dataset(nc_file, mode='r')
mpl.rcParams['figure.dpi'] = 150

lons = fh.variables['lon'][:]
lats = fh.variables['lat'][:]
time = fh.variables['time'][:]
pr = fh.variables['pr'][:,:,:]

pr_units = fh.variables['pr'].units

fh.close()


# Get some parameters for the Stereographic Projection
m = Basemap(projection = 'merc',
            llcrnrlon = -123.90209,
            llcrnrlat= 48.38405,
            urcrnrlon= -123.38891,
            urcrnrlat= 48.87273,
            area_thresh = 1,
            resolution = 'f')

# Because our lon and lat variables are 1D,
# use meshgrid to create 2D arrays
# Not necessary if coordinates are already in 2D arrays.
lon, lat = np.meshgrid(lons, lats)
xi, yi = m(lon, lat)

# Plot Data
cs = m.pcolor(xi,yi,np.squeeze(pr[0,:,:]), cmap = 'jet')

# Add Coastlines, States, and Country Boundaries
m.drawcoastlines()
m.drawstates()
m.drawcountries()
m.drawrivers()


# Add Colorbar
cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label(pr_units)

# Add Title
plt.title('something about precipitation')

plt.show()