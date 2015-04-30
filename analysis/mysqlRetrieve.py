# Script to retrieve and plot mysql data
#
# NOTE! To connect to remote mysql server with ssh tunneling, execute the 
# following in a separate command window:
#
#  ssh -L 3306:127.0.0.1:3306 <user>@<server>

import MySQLdb

def getAll(table):
	conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='Hejsan12', db='openhab')
	
	with conn:
		cur = conn.cursor()
		# Find out link between item and table name
		cur.execute("SELECT * FROM Items")
		tablesInv = cur.fetchall()
		# Inverse table and make it a dict
		tableDict = {v: k for k, v in tablesInv}
		# Get requested table
		cur.execute("SELECT * FROM Item%i" %tableDict[table])
		return cur.fetchall()

