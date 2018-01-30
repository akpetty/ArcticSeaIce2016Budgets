############################################################## 
# Date: 01/02/18
# Name: calcMonthlyBudgetsKimura.py
# Author: Alek Petty
# Description: Script to calculate monthly concentration budgets from the daily ice concentration and KIMURA ice drift data
# Input requirements: Daily ice concentration and KIMURA ice drift data
# Output: Monthly conc budgets

import matplotlib
from mpl_toolkits.basemap import Basemap, shiftgrid
import numpy as np
from pylab import *
from scipy.io import netcdf
import numpy.ma as ma

import commonFuncs as cF


m = Basemap(projection='npstere',boundinglat=53,lon_0=0, resolution='l'  )
#m = Basemap(projection='npstere',boundinglat=30.52,lon_0=0, resolution='l'  )


dataPath = '../../../../DATA'
figpath='../Figures/test/'
dataOutPath='../DataOutput/'
CStype='DRIFT_ASCAT_3DAY/'
extraStr='KIMURA'

latsI, lonsI = cF.get_psnlatslons(dataPath)
xptsI, yptsI =m(lonsI, latsI)


dx=100000.
dxStr=str(int(dx/1000))+'km'
print dxStr

alg=1

lonG, latG, xptsG, yptsG, nx, ny= cF.defGrid(m, dxRes=dx)

xptsG.dump(dataOutPath+'xptsG'+dxStr)
yptsG.dump(dataOutPath+'yptsG'+dxStr)
lonG.dump(dataOutPath+'lonG'+dxStr)
latG.dump(dataOutPath+'latG'+dxStr)

years=[2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
noDates=['201110', '201111', '201112', '201201','201202','201203','201204','201205','201206','201207','201208', '201209', '201210', '201211', '201412']

for year in years:
    print year
    for month in xrange(12):
        mstr = '%02d' %(month+1)
        dateStr=str(year)+mstr

        if (dateStr in noDates):
            break

        if (year>=2015):
            xptsC, yptsC, driftCmon, lonsC, latsC = cF.getKimuradriftMonthRaw(dataPath, year, month, m)
        else:
            xptsC, yptsC, driftCmon, lonsC, latsC = cF.getKimuradriftMonth(dataPath, year, month, m)
        
        numDays=driftCmon.shape[0]
        
        # should return array with nans not masked as needed for regridding.
        driftGmon=ma.masked_all((numDays, 2, nx, ny))
        iceConcGmon=ma.masked_all((numDays, nx, ny))
        for x in xrange(numDays):
            print 'Drift, mon:', month, 'day:', x

            driftCG = cF.smoothDriftDaily(xptsG, yptsG, xptsC, yptsC, latsC, driftCmon[x], sigmaG=0.75)

            driftGmon[x, 0]=driftCG[0]
            driftGmon[x, 1]=driftCG[1]

            #cF.plot_CSAT_DRIFT(m, xptsG, yptsG, driftGmon[x, 0], driftGmon[x, 1], sqrt(driftGmon[x, 0]**2+driftGmon[x, 1]**2), out=figpath+'/test'+dateStr+str(x)+'kd', units_lab=r'm s$^{-1}$', units_vec=r'm s$^{-1}$',
            #minval=0., maxval=0.3, base_mask=1,res=2, scale_vec=0.5, vector_val=0.1, cbar_type='max')
        
        if (year>2015):
            iceConcMon = cF.get_month_concSN_NRT(dataPath, year, month, alg=alg, pole='A', mask=1, maxConc=1)
        else:
            iceConcMon = cF.get_month_concSN_daily(dataPath, year, month, alg=alg, pole='A', mask=1, maxConc=1)

        #regrid all the daily ice concentrations onto CERSAT grid.
        for x in xrange(numDays):
            print 'Ice conc, mon:', month, 'day:', x
            


            iceConcG = griddata((xptsI.flatten(), yptsI.flatten()),iceConcMon[x].flatten(), (xptsG, yptsG), method='linear')
            iceConcMa=ma.masked_where(np.isnan(iceConcG), iceConcG)

            #cF.plot_conc(m, xptsG, yptsG, iceConcMa, figpath, 'testconc'+dateStr+str(x))

            #add dummy axis
            iceConcGmon[x] = iceConcMa
            

    #################### BUDGETS #########################

    # DIVERGENCE

        #gradient [0] returns row divs (y direction) then [1] gives column divs (x direction)   
        dvelxdx = np.gradient(driftGmon[:, 0,:, :], dx, axis=(2)) #2 here is the columns, so in the x direction?
        dvelydy = np.gradient(driftGmon[:, 1,:, :], dx, axis=(1))
        Div = -iceConcGmon*(dvelxdx+dvelydy)
        
        DivMean=ma.sum(Div*60*60*24., axis=0)# sum the div per day (note how we needed to multiply by seconds in a day)
        DivMean.dump(dataOutPath+'Divergence/DivMonths'+dxStr+dateStr+extraStr+'Alg'+str(alg))

    # ADVECTION

        dCdx = np.gradient(iceConcGmon, dx, axis=(2))
        dCdy = np.gradient(iceConcGmon, dx, axis=(1))
        Adv=-(driftGmon[:, 0,:, :]*dCdx)-(driftGmon[:, 1,:, :]*dCdy)

        AdvMean=ma.sum(Adv*60*60*24., axis=0)# sum the Adv per day (note how we needed to multiply by seconds in a day)
        AdvMean.dump(dataOutPath+'/Advection/AdvMonths'+dxStr+dateStr+extraStr+'Alg'+str(alg))

    # INTENSIFICATION

        iceConcInt=ma.masked_all((numDays-2, iceConcGmon.shape[1], iceConcGmon.shape[2]))
        for x in xrange(1, numDays-1):
            iceConcInt[x-1]=(iceConcGmon[x+1]-iceConcGmon[x-1])/2.

        IntMean=ma.sum(iceConcInt, axis=0)
        #IntMean=ma.masked_where(iceConcSeasonMean<0.15, IntMean)

        #convert from per day! to percent per year
        #IntMean=IntMean*(365*100.)
        IntMean.dump(dataOutPath+'/Intense/IceIntenseMonths'+dxStr+dateStr+extraStr+'Alg'+str(alg))














        