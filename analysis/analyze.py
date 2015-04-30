import pylab as pl
import mysqlRetrieve as sql

h = 5
ts = range(0,h*60*60,60)

i = 0.25e-3
C = 2.5
v0 = 3.3
Vb = [ -i*t/C+v0 for t in ts ]

#pl.figure()
#pl.plot(ts,Vb)
#deviceData = pl.array(sql.getAll('Scope_Level'))
deviceData = pl.array(sql.getAll('Battery_Level'))
pl.plot(deviceData[:,0], deviceData[:,1], '.-')
pl.show()
