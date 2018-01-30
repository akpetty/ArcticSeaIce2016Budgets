############################################################## 
# Date: 01/02/18
# Name: plotRatiosBox.py
# Author: Alek Petty
# Description: Script to produce box and whisker plots of sea ice area / sea ice extent (compactness)
# Input requirements: Sea ice area/extent data
# Output: Box and whisker plots of sea ice compactness

import matplotlib
matplotlib.use("AGG")
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

import commonFuncs as cF

dataPath = '../../../../DATA'
figpath='../Figures/'
dataOutPath='../DataOutput/Extent/'

rcParams['xtick.major.size'] = 2
rcParams['ytick.major.size'] = 2
rcParams['axes.linewidth'] = .5
rcParams['lines.linewidth'] = .4
rcParams['patch.linewidth'] = .5
rcParams['axes.labelsize'] = 8
rcParams['xtick.labelsize']=8
rcParams['ytick.labelsize']=8
rcParams['legend.fontsize']=8
rcParams['font.size']=8
rc('font',**{'family':'sans-serif','sans-serif':['Arial']})

monStrs=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def getRatioAlek(dataOutPath, month, alg):
	extent = loadtxt(dataOutPath+'iceExtMonths'+str(startYear)+str(endYear)+'Alg-'+str(alg))
	area = loadtxt(dataOutPath+'iceAreaMonths'+str(startYear)+str(endYear)+'Alg-'+str(alg))

	ratio=area[:, month]/extent[:, month]
	return ratio


years, extent = cF.get_ice_extentN(rawdatapath, pmonth, startYear, endYear, icetype=iceType, version='v2.1',  hemStr=hemStr)


startYear=2000
endYear=2016
years=np.arange(startYear, endYear+1, 1)

alg=1

if (alg==0):
	algStr='NASA Team'
if (alg==1):
	algStr='Bootstrap'

ratios=[]
ratios2016=[]
ranksExt=[]
for x in xrange(12):
	ratioT=getRatioAlek(dataOutPath, x, alg)
	ratios.append(ratioT[0:-1])
	ratios2016.append(ratioT[-1])

	# APPEND 2016 FOR RANK CALC
	#ratiosAll=hstack([ratioT, extent2016[0]]) 
	#ranksE = ratioT.argsort()
	rank2016=where(ratioT.argsort()==np.amax(ratioT.argsort()))[0][0]
	ranksExt.append(rank2016)




monStrs=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

fig = figure(figsize=(5.,2))
ax1=subplot(1, 1, 1)

bp=boxplot(ratios, positions=np.arange(12), widths=0.9, whis='range', sym='')

ax1.plot(np.arange(0., 12, 1), ratios2016, color='m', marker='x', markersize=3, linestyle='None')

for x in xrange(12):
	ratioStr= '%.2f' %ratios2016[x]
	ax1.annotate(ratioStr+'\n ('+str(ranksExt[x]+1)+')', xy=((x/12.)+0.04, 0.05), xycoords='axes fraction', horizontalalignment='center')
	#vars()['p'+str(x+1)]=ax1.axhline(y=(extents[x][-1]), xmin=(x/12.)+0.01, xmax=(x/12.)+0.09, color='m')
	

setp(bp['boxes'], color='black', lw=0.5)
setp(bp['whiskers'], color='black', ls='solid', lw=0.5)
setp(bp['fliers'], color='black', lw=0.5)
setp(bp['medians'], color='blue', lw=0.5)
setp(bp['caps'], color='black', lw=0.5)

ax1.annotate(algStr, xy=(0.01, 1.01), xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom')
	
ax1.set_ylabel('Compactness', labelpad=4)
ax1.set_xlim(-0.5, 11.5)
ax1.set_xticks(np.arange(12))
ax1.set_xticks(np.arange(-0.5, 12, 1), minor=True)
ax1.set_xticklabels(monStrs)
#ax1.set_xlabel('Month')
#ylim(0, np.amax(np.ceil(extents[2])))
ylim(0.45, 0.95)

ax1.xaxis.grid(True, linestyle='-', which='minor', color='lightgrey',
               alpha=0.5)

subplots_adjust(left=0.08, right=0.98, bottom=0.12, top=0.93, hspace=0)

savefig(figpath+'/areaExtentRatio'+str(startYear)+str(endYear)+algStr+'Box.pdf', dpi=300)
close(fig)









