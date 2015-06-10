import pylab as pl
import csvRetrieve as csv

deviceData = pl.array(csv.getAll('slowRiseTimeTest.csv'))

# Required slope
slope = 1.8/60e-6

ix1 = len(deviceData)-500
ix2 = len(deviceData)-1

x1 = deviceData[ix1,0]
x2 = deviceData[ix2,0]
y1 = deviceData[ix1,1]
y2 = deviceData[ix2,1]

k = (y2-y1)/(x2-x1)
m = y1-k*x1

x0 = deviceData[0,0]
y0 = k*x0+m
xN = deviceData[-1,0]
yN = k*xN+m

pl.plot(deviceData[:,0], deviceData[:,1], '.-', label="VCC Voltage")
pl.plot([x0, xN], [y0, yN], label="Slope: %f V/s (req: %i V/s)" %(k,slope))
pl.legend(loc=4)
pl.show()
