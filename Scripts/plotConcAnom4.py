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


m = Basemap(projection='npstere',boundinglat=53,lon_0=0, resolution='l' ,round=False )
#m = Basemap(projection='npstere',boundinglat=30.52,lon_0=0, resolution='l'  )

dataPath = '../../../../DATA'
figpath='../Figures/'
dataOutPath='../DataOutput/Conc/'

latsI, lonsI = cF.get_psnlatslons(dataPath)
xptsI, yptsI =m(lonsI, latsI)

startYear=2000
endYear=2015
numYears=endYear-startYear+1
startMonth=8
alg=0

ConcMonths=ma.masked_all((numYears, 4, xptsI.shape[0], xptsI.shape[1]))
ConcAnom=ma.masked_all((4, xptsI.shape[0], xptsI.shape[1]))

for year in xrange(startYear, endYear+1):
	for month in xrange(startMonth, 12):
		mstr = '%02d' %(month+1)
		dateStr=str(year)+mstr
	
		ConcMonths[year-startYear, month-startMonth]=load(dataOutPath+'iceConc'+dateStr+'Alg'+str(alg))

ConcMean=ma.mean(ConcMonths, axis=0)


for month in xrange(startMonth, 12):
	ConcMean[month-startMonth]=ma.masked_where(latsI>86.5, ConcMean[month-startMonth])
	ConcAnomT=ConcMonths[-1, month-startMonth]-ConcMean[month-startMonth]
	# Mask the pole hole
	ConcAnom[month-startMonth]=ma.masked_where(latsI>86.5, ConcAnomT)


monStrs=['Sep', 'Oct', 'Nov', 'Dec']

maxval=1
minval=-1
norm = cF.MidPointNorm_Good(midpoint=0)

fig = figure(figsize=(5.6,1.6))
for x in xrange(4):

	subplot(1,4,x+1) 
	axT=gca()
	#conc per month
	im1 = m.pcolormesh(xptsI , yptsI, ConcAnom[x], cmap=plt.cm.RdBu_r, norm=norm, vmin=minval, vmax=maxval, shading='gouraud', zorder=1, rasterized=True)
	m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=10)
	m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=10)
	m.fillcontinents(color='0.9',lake_color='grey', zorder=7)
	m.drawcoastlines(linewidth=0.15, zorder=5, color='k')
	axT.annotate(monStrs[x], xy=(0.04, 0.9 ),xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom', zorder=10)

cax = fig.add_axes([0.925, 0.2, 0.02, 0.6])
cbar = colorbar(im1,cax=cax, orientation='vertical', extend='both', use_gridspec=True)
cbar.solids.set_rasterized(True)
cbar.set_label('A', labelpad=-3, rotation=0)
cbar.set_ticks([minval, maxval])

subplots_adjust(bottom=0.01, left=0.01, wspace=0.03, hspace=0.02, top=0.99, right=0.92 )

savefig(figpath+'/conc'+str(startYear)+str(endYear)+'Alg'+str(alg)+'4anom.png', dpi=300)
close(fig)





