############################################################## 
# Date: 01/02/18
# Name: plotFluxDivergenceAnom.py
# Author: Alek Petty
# Description: Script to produce plots of monthly flux diveregence anomalies
# Input requirements: Flux divergence data from calcMonthlyBudgetsKimura.py
# Output: Maps of monthly flux divergence anomalies

import matplotlib
matplotlib.use("AGG")
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

import commonFuncs as cF


rcParams['ytick.major.size'] = 2
rcParams['axes.linewidth'] = .5
rcParams['lines.linewidth'] = .5
rcParams['patch.linewidth'] = .5
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8 
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

m = Basemap(projection='npstere',boundinglat=54,lon_0=0, resolution='l' )

dataPath = '../../../../DATA'
figpath='../Figures/'
dataOutPath='../DataOutput/'
dataOutPathConc='../DataOutput/Conc/'
latsI, lonsI = cF.get_psnlatslons(dataPath)
xptsI, yptsI =m(lonsI, latsI)

extraStr='KIMURA'

alg=1


dx=100000.
dxStr=str(int(dx/1000))+'km'
print dxStr

lonG=load(dataOutPath+'lonG'+dxStr)
latG=load(dataOutPath+'latG'+dxStr)
xptsG, yptsG=m(lonG, latG)


years=[2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]

noDates=['201110', '201111', '201112', '201201','201202','201203','201204','201205','201206','201207','201208', '201209', '201210', '201211', '201412']


numYears=size(years)

FluxDivMonths=ma.masked_all((numYears, 12, xptsG.shape[0], xptsG.shape[1]))
FluxDivAnom=ma.masked_all((12, xptsG.shape[0], xptsG.shape[1]))
Concmonth=[]

y=0
for year in years:
	for month in xrange(0, 12):
		mstr = '%02d' %(month+1)
		dateStr=str(year)+mstr
		if (dateStr in noDates):
			break
		AdvmonthsT=load(dataOutPath+'/Advection/AdvMonths'+dxStr+dateStr+extraStr+'Alg'+str(alg))
		DivmonthsT=load(dataOutPath+'/Divergence/DivMonths'+dxStr+dateStr+extraStr+'Alg'+str(alg))
		FluxDivT=AdvmonthsT+DivmonthsT
		FluxDivT=ma.masked_where(latG>88, FluxDivT)
		FluxDivMonths[y, month]=FluxDivT
	y+=1
		
FluxDivMean=ma.mean(FluxDivMonths[0:-1], axis=0)

for month in xrange(0, 12):
	FluxDivAnom[month]=FluxDivMonths[-1, month]-FluxDivMean[month]
	mstr = '%02d' %(month+1)
	dateStr=str(year)+mstr
	Concmonth.append(load(dataOutPathConc+'iceConc'+dateStr+'Alg'+str(alg)))

monStrs=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

maxval=1
minval=-1
fig = figure(figsize=(5.1,5.9))
for x in xrange(12):

	subplot(4,3,x+1) 
	axT=gca()
	#conc per month
	im1 = m.pcolormesh(xptsG , yptsG, FluxDivAnom[x], cmap=plt.cm.RdBu_r, vmin=minval, vmax=maxval, shading='gouraud', zorder=1, rasterized=True)
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

savefig(figpath+'/fluxDiv'+str(years[0])+str(years[-1])+'Alg'+str(alg)+'anom.png', dpi=300)
close(fig)





