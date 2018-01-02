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








