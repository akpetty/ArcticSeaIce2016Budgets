############################################################## 
# Date: 01/02/18
# Name: commonFuncs.py
# Author: Alek Petty
# Description: Common functions needed for budget/ranking scripts


import matplotlib
matplotlib.use("AGG")
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma
from matplotlib import rc
from glob import glob
import pandas as pd
from  matplotlib import cbook
from scipy import stats
import time
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from netCDF4 import Dataset
from scipy.spatial import cKDTree as KDTree
from scipy.interpolate import griddata
from scipy.ndimage.filters import gaussian_filter

def get_psnlatslons(data_path):
	mask_latf = open(data_path+'/OTHER/psn25lats_v3.dat', 'rb')
	mask_lonf = open(data_path+'/OTHER/psn25lons_v3.dat', 'rb')
	lats_mask = reshape(fromfile(file=mask_latf, dtype='<i4')/100000., [448, 304])
	lons_mask = reshape(fromfile(file=mask_lonf, dtype='<i4')/100000., [448, 304])

	return lats_mask, lons_mask

def get_month_concSN_NRT(datapath, year, month, alg=0, pole='A',  mask=1, maxConc=0, lowerConc=0, monthMean=0):
	if (alg==0):
		team = 'NASA_TEAM'
		team_s = 'nt'
		header = 300
		datatype='uint8'
		scale_factor=250.
	if (alg==1):
		team = 'BOOTSTRAP'
		team_s = 'NH'
		header = 0
		datatype='<i2'
		scale_factor=1000.
	
	if (pole=='A'):
		poleStr='ARCTIC'
		rows=448
		cols=304
	if (pole=='AA'):
		poleStr='ANTARCTIC'
		rows=332
		cols=316

	month_str = '%02d' % (month+1)
	year_str=str(year)
	files = glob(datapath+'/ICE_CONC/'+team+'/'+poleStr+'/NRT/*'+str(year)+month_str+'*')
	
	print 'Num conc files:', size(files), 'in month:'+month_str
	ice_conc = ma.masked_all((size(files), rows, cols))
	
	for x in xrange(size(files)):
		fd = open(files[x], 'r')
		data = fromfile(file=fd, dtype=datatype)
		data = data[header:]
		#FIRST 300 FILES ARE HEADER INFO
		ice_conc[x] = reshape(data, [rows, cols])
		
	#divide by 250 to express in concentration
	ice_conc = ice_conc/scale_factor
	#GREATER THAN 250 is mask/land etc
	
	if (mask==1):
		ice_conc = ma.masked_where(ice_conc>1., ice_conc)
	
	if (maxConc==1):
		ice_conc = ma.where(ice_conc>1.,0, ice_conc)

	if (lowerConc==1):
		ice_conc = ma.where(ice_conc<0.15,0, ice_conc)

	if (monthMean==1):
		ice_conc=ma.mean(ice_conc, axis=0)

	return ice_conc
	

	

def get_month_concSN_daily(datapath, year, month, alg=0, pole='A', vStr='v1.1', mask=1, maxConc=0, lowerConc=0, monthMean=0):
	if (alg==0):
		team = 'NASA_TEAM'
		team_s = 'nt'
		header = 300
		datatype='uint8'
		scale_factor=250.
	if (alg==1):
		team = 'BOOTSTRAP'
		team_s = 'bt'
		header = 0
		datatype='<i2'
		scale_factor=1000.
	
	if (pole=='A'):
		poleStr='ARCTIC'
		rows=448
		cols=304
	if (pole=='AA'):
		poleStr='ANTARCTIC'
		rows=332
		cols=316

	month_str = '%02d' % (month+1)
	year_str=str(year)
	files = glob(datapath+'/ICE_CONC/'+team+'/'+poleStr+'/daily/'++str(year)+'/'+team_s+'_'+str(year)+month_str+'*'+vStr+'*')
	

	print 'Num conc files:', size(files), 'in month:'+month_str
	ice_conc = ma.masked_all((size(files), rows, cols))
	
	for x in xrange(size(files)):
		fd = open(files[x], 'r')
		data = fromfile(file=fd, dtype=datatype)
		data = data[header:]
		#FIRST 300 FILES ARE HEADER INFO
		ice_conc[x] = reshape(data, [rows, cols])
		
	#divide by 250 to express in concentration
	ice_conc = ice_conc/scale_factor
	#GREATER THAN 250 is mask/land etc

	if (mask==1):
		ice_conc = ma.masked_where(ice_conc>1., ice_conc)
	
	if (maxConc==1):
		ice_conc = ma.where(ice_conc>1.,0, ice_conc)

	if (lowerConc==1):
		ice_conc = ma.where(ice_conc<0.15,0, ice_conc)

	if (monthMean==1):
		ice_conc=ma.mean(ice_conc, axis=0)

	return ice_conc

def get_pmask(year, month):
	#remove half a degree as gridding around the pole hole edge
	if (year<1987):
		pmask=84.4
	elif((year==1987)&(month<=6)):
		pmask=84.4
	elif ((year==1987)&(month>6)):
		pmask=86.7
	elif ((year>1987)&(year<2008)):
		pmask=87.2
	else:
		pmask=89.2
	
	return pmask

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