############################################################## 
# Date: 01/01/16
# Name: calc_cersat_driftSTORM.py
# Author: Alek Petty
# Description: Script to plot SEB data from Linette
# Input requirements: SEB data
# Output: map of an SEB term
import matplotlib
matplotlib.use("AGG")

from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma
from matplotlib import rc
from glob import glob
from netCDF4 import Dataset
from scipy.interpolate import griddata
import sys
sys.path.append('../../common/')
import commonFuncs as cF

rcParams['ytick.major.size'] = 2
rcParams['axes.linewidth'] = .5
rcParams['lines.linewidth'] = .5
rcParams['patch.linewidth'] = .5
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8 
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

dataPath = '../../../../DATA'
figpath='../Figures/'
dataOutPath='../DataOutput/Intense/'
dataOutPathConc='../DataOutput/Conc/'
m = Basemap(projection='npstere',boundinglat=53,lon_0=0, resolution='l')
#m = Basemap(projection='npstere',boundinglat=30.52,lon_0=0, resolution='l'  )

latsI, lonsI = cF.get_psnlatslons(dataPath)
xptsI, yptsI =m(lonsI, latsI)

alg=0

year=2016
Intmonth=[]
for month in xrange(0, 12):
	mstr = '%02d' %(month+1)
	dateStr=str(year)+mstr
	
	Intmonth.append(load(dataOutPath+'iceIntense'+dateStr+'Alg'+str(alg)))

Concmonth=[]
for month in xrange(0, 12):
	mstr = '%02d' %(month+1)
	dateStr=str(year)+mstr
	Concmonth.append(load(dataOutPathConc+'iceConc'+dateStr+'alg'+str(alg)))


monStrs=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

maxval=1.
minval=-1.
fig = figure(figsize=(5.1,5.9))
for x in xrange(12):

	subplot(4,3,x+1) 
	axT=gca()
	#conc per month
	im1 = m.pcolormesh(xptsI , yptsI, Intmonth[x], cmap=plt.cm.RdBu_r, vmin=minval, vmax=maxval, shading='gouraud', zorder=1, rasterized=True)
	im2 = m.contour(xptsI , yptsI, Concmonth[x], levels=[0.15], colors='k', zorder=2)
	m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=10)
	m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=10)
	m.fillcontinents(color='0.9',lake_color='grey', zorder=7)
	m.drawcoastlines(linewidth=0.15, zorder=5, color='k')
	axT.annotate(monStrs[x], xy=(0.04, 0.9 ),xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom', zorder=10)

cax = fig.add_axes([0.9, 0.43, 0.02, 0.14 ])
cbar = colorbar(im1,cax=cax, orientation='vertical', extend='both', use_gridspec=True)
cbar.solids.set_rasterized(True)
cbar.set_label(r'$\Delta$A/mon', labelpad=-4)
cbar.set_ticks([minval, maxval])

subplots_adjust(bottom=0.01, left=0.01, wspace=0.01, hspace=0.02, top=0.99, right=0.9 )

savefig(figpath+'/intense'+str(year)+'Alg'+str(alg)+'.png', dpi=300)
close(fig)





