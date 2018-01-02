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
figpath='../Figures/Conc/'
dataOutPath='../DataOutput/Extent/'

m = Basemap(projection='npstere',boundinglat=60,lon_0=0, resolution='l', round=True  )


def getExtentAreaFromConc(iceConcMon):
	iceConcMon=ma.masked_where(iceConcMon<=0.15, iceConcMon)
	iceConcMon=ma.masked_where(ice_flag>=1.5, iceConcMon)

	concHole=ma.mean(iceConcMon[(lats>pmask-0.5) & (lats<pmask)])

	iceConcMonP = ma.where((lats >=pmask), 1., iceConcMon)
	iceConcMonA = ma.where((lats >=pmask), concHole, iceConcMon)
	#zeroCounts= (iceConcDays >1).sum(axis=0)
	#iceConcDays = where(iceConcDays>1.,0, iceConcDays)

	#iceConcDays=where((lats >=pmask), 1, iceConcDays)
	#iceConcDays= where((iceConcDays <=0.15), 0, iceConcDays)

	#iceConcMon=np.mean(iceConcDays, axis=0)
	
	#iceConcMon= where((iceConcMon <=0.15), 0, iceConcMon)


	#iceConcCount=ma.count(iceConcDays, axis=0)
	#iceConcMon= where((zeroCounts >=10), 0, iceConcMon)
	#iceConcMon=ma.masked_where(zeroCounts>10, iceConcMon)
		
	
	#plot_conc(xpts, ypts, iceConcMonP, dateStr+'Alg'+str(alg)+'Ext3')
	#plot_conc(xpts, ypts, iceConcMonA, dateStr+'Alg'+str(alg)+'Area3')

	iceExtent = ma.sum(ma.where((iceConcMonP >0.15), 1, 0)*areaF)
	iceArea = ma.sum(iceConcMonA*areaF)
	return iceExtent, iceArea

def plot_conc(xpts, ypts, concT, dateStr):
	textwidth=4.
	fig = figure(figsize=(textwidth,textwidth))
	subplots_adjust(bottom=0.01, top=0.99, left=0.01, right=0.99)


	#ax1=subplot(1, 3, 1)
	minval=0
	maxval=1
	#ADD GRIDSIZE=NUMBER KWARG TO HEXBIN IF YOU WANT TO CHANGE SIZE OF THE BINS
	im1 = m.pcolormesh(xpts , ypts, concT, cmap=cm.viridis, vmin=minval, vmax=maxval,shading='flat', zorder=2)
	#im2 = m.contour(xpts , ypts, ma.mean(Pressure, axis=0),levels=[990, 1000, 1100],colors='k', zorder=4)
	m.drawcoastlines(linewidth=0.5, zorder=5)
	m.drawparallels(np.arange(90,-90,-10), linewidth = 0.25, zorder=3)
	m.drawmeridians(np.arange(-180.,180.,30.), linewidth = 0.25, zorder=3)
	#m.plot(xptsR, yptsR, '--', linewidth = 2, color='k', zorder=5)

	#ADD COLORBAR TO MAP
	#bbox_args = dict(fc="white")
	#ax1.annotate('.                   \n             \n        ', xy=(0.02, 0.98), bbox=bbox_args,xycoords='axes fraction', horizontalalignment='left', verticalalignment='top', zorder=10)

	#ax1.annotate(files[x][-8:-4]+'-'+files[x][-4:-2]+'-'+files[x][-2:], xy=(0.98, 0.98), bbox=bbox_args,xycoords='axes fraction', horizontalalignment='right', verticalalignment='top', zorder=10)
	label_str='Conc'
	#ax1.annotate('AIRS temp anomaly from 2003-2014 mean', xy=(0.02, 0.02), bbox=bbox_args,xycoords='axes fraction', horizontalalignment='left', verticalalignment='bottom', zorder=10)
	cax = fig.add_axes([0.02, 0.88, 0.25, 0.035])
	cbar = colorbar(im1,cax=cax, orientation='horizontal', extend='both', use_gridspec=True)
	cbar.set_label(label_str, labelpad=1)
	cbar.set_ticks(np.arange(minval, maxval+1, 75))
	cbar.solids.set_rasterized(True)
	#SHIFT COLOR SPACE SO OFF WHITE COLOR IS AT 0 m
	#cbar.set_clim(minval, maxval)
	savefig(figpath+'/concT'+dateStr+'.png', dpi=300)
	close(fig)



startYear=1979
endYear=2016
numYears=endYear-startYear+1

startMon=9
endMon=9
numMons=endMon-startMon+1

alg=0 #0 is NT, 1 is BT


areaF=reshape(fromfile(file=open(dataPath+'/OTHER/psn25area_v3.dat', 'rb'), dtype='<i4')/1000., [448, 304])/1e6

lats, lons = cF.get_psnlatslons(dataPath)
xpts, ypts=m(lons, lats)


#iceExtMon=np.zeros((numYears, numMons))
#iceAreaMon=np.zeros((numYears, numMons))

for month in xrange(startMon, endMon+1):
	iceExtMon=[]
	iceAreaMon=[]
	for year in xrange(startYear, endYear+1):
	

		mstr = '%02d' %(month+1)
		dateStr=str(year)+mstr
		pmask= cF.get_pmask(year, month)
		#pmask=89.2
		f = Dataset(dataPath+'/OTHER/NIC_valid_ice_mask.N25km.'+mstr+'.1972-2007.nc', 'r')
		ice_flag = f.variables['valid_ice_flag'][:]

		print dateStr
		if (year>2015):
			iceConcMon = cF.get_month_concSN_NRT(dataPath, year, month, alg=alg, pole='A',  mask=1, lowerConc=0, monthMean=1)
		else:
			iceConcMon = cF.get_month_concSN_daily(dataPath, year, month, alg=alg, pole='A',  mask=1,  lowerConc=0, monthMean=1)
			#iceConcMon = cF.get_month_concSN(dataPath, year, month, alg=alg, pole='A')

		
		iceExtT, iceAreaT = getExtentAreaFromConc(iceConcMon)
		

		iceExtMon.append(iceExtT)
		iceAreaMon.append(iceAreaT)

		#iceConcMon = ice_conc.filled(0)
		#for x in xrange(iceConcMon.shape[0]):

		#	iceConcMon[x] = where((ice_flag >=1.5), 0, ice_conc)
		#	iceConcMon[x] = where((ice_conc <=0.15), 0, ice_conc)
		#getExtent(iceConcMon)

		#i
		#ice_conc_month=np.mean(ice_conc, axis=0)
		

		

	
	savetxt(dataOutPath+'iceExtMonths'+str(startYear)+str(endYear)+'-'+mstr+'Alg-'+str(alg)+'', iceExtMon)
	savetxt(dataOutPath+'iceAreaMonths'+str(startYear)+str(endYear)+'-'+mstr+'Alg-'+str(alg)+'', iceAreaMon)

	
#print iceExtMon, iceAreaMon

		#IntMean=ma.mean(iceConcMon, axis=0)
		#IntMean=ma.masked_where(ma.mean(iceConcMon, axis=0)<0.15, IntMean)

#savetxt(dataOutPath+'iceExtMonths'+str(startYear)+str(endYear)+'Alg-'+str(alg), iceExtMon)
#savetxt(dataOutPath+'iceAreaMonths'+str(startYear)+str(endYear)+'Alg-'+str(alg), iceAreaMon)








