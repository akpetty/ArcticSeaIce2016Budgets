############################################################## 
# Date: 01/02/18
# Name: calcIceConc.py
# Author: Alek Petty
# Description: Script to calculate monthly sea ice concentration from daily data (e.g. NRT data)
# Input requirements: Daily sea ice conentration data (NASA Team or Bootstrap)
# Output: Monthly sea ice concentrations

import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

import commonFuncs as cF

dataPath = '../../../../DATA'
figpath='../Figures/'
dataOutPath='../DataOutput/Conc/'


startYear=1979
endYear=2016
alg=1

for year in xrange(startYear, endYear+1):
	for month in xrange(0, 12):
		mstr = '%02d' %(month+1)
		dateStr=str(year)+mstr
		print dateStr
		if (year>2015):
			iceConcMon = cF.get_month_concSN_NRT(dataPath, year, month, alg=alg, pole='A', daily=1, mask=1)
		else:
			iceConcMon = cF.get_month_concSN_daily(dataPath, year, month, alg=alg, pole='A', daily=1, mask=1)

		IntMean=ma.mean(iceConcMon, axis=0)
		#IntMean=ma.masked_where(ma.mean(iceConcMon, axis=0)<0.15, IntMean)
		IntMean.dump(dataOutPath+'iceConc'+dateStr+'Alg'+str(alg))








