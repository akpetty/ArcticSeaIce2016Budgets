############################################################## 
# Date: 01/02/18
# Name: calcExtentAreaFromDays.py
# Author: Alek Petty
# Description: Script to calculate sea ice extent/area from DAILY sea ice concentration data
# Input requirements: Sea ice conentration data (NASA Team or Bootstrap)
# Output: Indices of sea ice extent and area

import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

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


	iceExtent = ma.sum(ma.where((iceConcMonP >0.15), 1, 0)*areaF)
	iceArea = ma.sum(iceConcMonA*areaF)
	return iceExtent, iceArea



startYear=2000
endYear=2016
numYears=endYear-startYear+1

startMon=0
endMon=11
numMons=endMon-startMon+1

alg=1 #0 is NT, 1 is BT


areaF=reshape(fromfile(file=open(dataPath+'/OTHER/psn25area_v3.dat', 'rb'), dtype='<i4')/1000., [448, 304])/1e6

lats, lons = cF.get_psnlatslons(dataPath)
xpts, ypts=m(lons, lats)


#iceExtMon=np.zeros((numYears, numMons))
#iceAreaMon=np.zeros((numYears, numMons))

for month in xrange(startMon, endMon+1):
	mstr = '%02d' %(month+1)
	iceExtMon=[]
	iceAreaMon=[]

	for year in xrange(startYear, endYear+1):
		
		dateStr=str(year)+mstr
		pmask= cF.get_pmask(year, month)
		#pmask=89.2
		f = Dataset(dataPath+'/OTHER/NIC_valid_ice_mask.N25km.'+mstr+'.1972-2007.nc', 'r')
		ice_flag = f.variables['valid_ice_flag'][:]

		print dateStr
		if (year>2015):
			iceConcMon = cF.get_month_concSN_NRT(dataPath, year, month, alg=alg, pole='A',  mask=1, maxConc=0, lowerConc=0, monthMean=0)
		else:
			iceConcMon = cF.get_month_concSN_daily(dataPath, year, month, alg=alg, pole='A',  mask=1, maxConc=0, lowerConc=0, monthMean=0)

		iceExtTs=[]
		iceAreaTs=[]
		for x in xrange(iceConcMon.shape[0]):
			iceExtT, iceAreaT = getExtentAreaFromConc(iceConcMon[x])
			iceExtTs.append(iceExtT)
			iceAreaTs.append(iceAreaT)

		iceExtMon.append(mean(iceExtTs))
		iceAreaMon.append(mean(iceAreaTs))


	savetxt(dataOutPath+'iceExtMonths'+str(startYear)+str(endYear)+'-'+mstr+'Alg-'+str(alg)+'FromDays', iceExtMon)
	savetxt(dataOutPath+'iceAreaMonths'+str(startYear)+str(endYear)+'-'+mstr+'Alg-'+str(alg)+'FromDays', iceAreaMon)

	
	
print iceExtMon, iceAreaMon






