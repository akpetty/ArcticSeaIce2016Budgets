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

def get_ice_extent_petty(dataOutPath, month, start_year, end_year, icetype='extent', alg=0):
	""" Get Arctic sea ice extent using Petty/NSIDC method

	Data downloaded from the NSIDC and extent caluclated using the ASI

	Can also get ice area if icetype set to 'area', 
	   but beware of variable pole hole contaminating Arctic data

	"""

	if (icetype=='area'):
		typeStr='Area'
	else:
		typeStr='Ext'
	extentT = loadtxt(dataOutPath+'ice'+typeStr+'Months'+str(1979)+str(2016)+'Alg-'+str(alg))[:, Month]
	extent = extentT[start_year-1979:end_year-1979+1]

	years=np.arange(start_year, end_year, 1)
	

	return years, extent

def get_ice_extentN(rawdatapath, Month, start_year, end_year, icetype='extent', version='', hemStr='N'):
	""" Get Arctic sea ice extent

	Data downlaoded from the NSIDC Arctic Sea Ice Index.

	Can also get ice area if icetype set to 'area', 
	   but beware of variable pole hole contaminating Arctic data

	"""
	Month_str = '%02d' %Month
	extent_data_path=rawdatapath+'/ICE_CONC/SeaIceIndex/'+hemStr+'_'+Month_str+'_extent_'+version+'.csv'
	ice_extent_data=pd.read_csv(extent_data_path,names=['year', 'extent', 'area'],skiprows=1, usecols=[0, 4, 5])
	#ice_extent_data = np.loadtxt(extent_data_path, delimiter=',',skiprows=1)
	Extent = ice_extent_data[icetype]
	Year = ice_extent_data['year']
	
	#Years=array(Year[start_year-1979:end_year-1979+1])
	Years=array(Year[(Year>=start_year)&(Year<=end_year)])
	Extents=array(Extent[(Year>=start_year)&(Year<=end_year)])

	Years=Years[where(Extents>0)]
	Extents=Extents[where(Extents>0)]

	#Extents=ma.masked_where(Extents<0, Extents)
	#Extent=array(Extent[start_year-1979:end_year-1979+1])

	return Years, Extents


years, extent = ff.get_ice_extentN(rawdatapath, pmonth, startYear, endYear, icetype=iceType, version='v2.1',  hemStr=hemStr)



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









