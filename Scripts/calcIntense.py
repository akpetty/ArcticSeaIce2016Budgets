############################################################## 
# Date: 01/02/18
# Name: calcIntense.py
# Author: Alek Petty
# Description: Script to calculate ice intensification from the daily ice concentration data
# Input requirements: Sea ice concentration data (daily)
# Output: Monthly ice intensification estimates

import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

import commonFuncs as cF

dataPath = '../../../../DATA'
figpath='../Figures/'
dataOutPath='../DataOutput/Intense/'


startYear=2000
endYear=2016

alg=1 # 0 NASA Team, 1 Bootstrap

for year in xrange(startYear, endYear+1):
	for month in xrange(0, 12):
		mstr = '%02d' %(month+1)
		dateStr=str(year)+mstr
		print dateStr
		if (year>2015):
			iceConcMon = cF.get_month_concSN_NRT(dataPath, year, month, alg=alg, pole='A', mask=1, maxConc=1)
		else:
			iceConcMon = cF.get_month_concSN_daily(dataPath, year, month, alg=alg, pole='A', mask=1, maxConc=1)

		numDays=iceConcMon.shape[0]
		iceConcInt=ma.masked_all((numDays-2, iceConcMon.shape[1], iceConcMon.shape[2]))

		#loop over all days (minus the start and end day) of each month
		for x in xrange(1, numDays-1):
			iceConcInt[x-1]=(iceConcMon[x+1]-iceConcMon[x-1])/2. # Note the x-1 in the Int array is there to move index back to 0
		
		IntMean=ma.sum(iceConcInt, axis=0)
		#IntMean=ma.masked_where(ma.mean(iceConcMon, axis=0)<0.15, IntMean)
		IntMean.dump(dataOutPath+'iceIntense'+dateStr+'alg'+str(alg))








