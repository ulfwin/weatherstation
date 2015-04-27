# Script to retrieve and plot mysql data
#
# NOTE! To connect to remote mysql server with ssh tunneling, execute the 
# following in a separate command window:
#
#  ssh -L 3306:127.0.0.1:3306 <user>@<server>

import MySQLdb
import pylab as pl

conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='Hejsan12', db='openhab')

with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Item1")
        rows = pl.array(cur.fetchall())
        pl.plot(rows[100:,0], rows[100:,1], '.-')
	#print pl.array(rows[:10])[:,0]
	pl.show()
