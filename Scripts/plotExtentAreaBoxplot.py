############################################################## 
# Date: 01/02/18
# Name: plotExtentAreaBoxplot.py
# Author: Alek Petty
# Description: Script to produce box and whisker plots of sea ice extent/area
# Input requirements: Sea ice conentration data (NASA Team or Bootstrap)
# Output: Box and whisker plots

import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

import commonFuncs as cF

rcParams['xtick.major.size'] = 2
rcParams['ytick.major.size'] = 2
rcParams['axes.linewidth'] = .5
rcParams['lines.linewidth'] = .5
rcParams['patch.linewidth'] = .5
rcParams['axes.labelsize'] = 8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=7
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

dataOutPath='../DataOutput/Extent/'
figpath='../Figures/'

def getExtentArea(dataOutPath, month, alg, outType):
	extent = loadtxt(dataOutPath+'ice'+outType+'Months'+str(startYear)+str(endYear)+'Alg-'+str(alg))

	return extent[:, month]


icetype='extent'
alg=0

if (icetype=='extent'):
	outType='Ext'
	labelStr=r'Sea ice extent (M km$^2$)'
	ymax=16
if (icetype=='area'):
	outType='Area'
	labelStr=r'Sea ice area (M km$^2$)'
	ymax=16

if (alg==0):
	algStr='NASA Team'
if (alg==1):
	algStr='Bootstrap'

extraStr=''


startYear=2000
endYear=2016
years=np.arange(startYear, endYear+1, 1)
extents=[]
ranksExt=[]
extents2016=[]
for month in xrange(12):
	#extentT = getExtentArea(dataOutPath, month, alg, outType)
	years, extentT = cF.getIceExtentAreaPetty(dataOutPath, month+1, 2000, 2016, icetype=icetype, alg=alg, extraStr=extraStr)

	extents.append(extentT[0:-1])
	extents2016.append(extentT[-1])

	# APPEND 2016 FOR RANK CALC
	rank2016=where(extentT.argsort()==np.amax(extentT.argsort()))[0][0]
	ranksExt.append(rank2016)
	
	

monStrs=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig = figure(figsize=(5.,2))
ax1=subplot(1, 1, 1)

bp=boxplot(extents, positions=np.arange(12), widths=0.9, whis='range', sym='')

for x in xrange(12):
	extents2016Str='%0.2f' %extents2016[x]
	ax1.annotate(extents2016Str+'\n ('+str(ranksExt[x]+1)+')', xy=((x/12.)+0.04, 0.025), xycoords='axes fraction', horizontalalignment='center')
	
ax1.annotate(algStr, xy=(0.01, 1.01), xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom')
	
	
ax1.plot(np.arange(0., 12, 1), extents2016, color='m', marker='x', markersize=3, linestyle='None')
	
setp(bp['boxes'], color='black', lw=0.5)
setp(bp['whiskers'], color='black', ls='solid', lw=0.5)
setp(bp['fliers'], color='black', lw=0.5)
setp(bp['medians'], color='blue', lw=0.5)
setp(bp['caps'], color='black', lw=0.5)


ax1.set_ylabel(labelStr, labelpad=4)
ax1.set_xlim(-0.5, 11.5)
ax1.set_xticks(np.arange(12))
ax1.set_xticks(np.arange(-0.5, 12, 1), minor=True)
ax1.set_xticklabels(monStrs)

ylim(0, ymax)

ax1.xaxis.grid(True, linestyle='-', which='minor', color='lightgrey',
               alpha=0.5)



subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.93, hspace=0)

savefig(figpath+'/'+icetype+str(startYear)+str(endYear)+'Alg-'+str(alg)+'allmonths'+extraStr+'.pdf', dpi=300)
close(fig)
