import pexpect
import time
import sys
import datetime

gatttool_cmd = 'gatttool -b DD:4F:3B:2C:A0:5B -I'
send2OH = 'curl --header "Content-Type: text/plain" --request PUT --data "%s" http://localhost:8080/rest/items/Battery_Level/state'

# Start gatttool
con = pexpect.spawn(gatttool_cmd)
con.expect('\[LE\]>', timeout=1)
print "Started gatttool"

# Connect to device, keep trying if timed out
retry = 0
while 1:
	con.sendline('connect')
	retry += 1
	sys.stdout.write("%s Trying to connect (try nr %i)\r" %(str(datetime.datetime.now()), retry))
	sys.stdout.flush()
	con.expect(['\[CON\].*>', 'Connection refused', pexpect.TIMEOUT], timeout=60)
	if 'Connection refused' in con.after:
		pass

	elif con.after == pexpect.TIMEOUT:
		# Restart gatttool
		print "Restarting gatttool..."
		con.sendline('exit')
		con = pexpect.spawn(gatttool_cmd)
		con.expect('\[LE\]>', timeout=1)
		print "Started gatttool"
		
	elif '[CON]' in con.after:
		sys.stdout.write("\n")
		print "Successfully Connected to Bluetooth Device"
		retry = 0

		# Read data, go back to trying to connect if it fails
		connected = 1
		measNr = 0
		while connected == 1:
			con.sendline('char-read-uuid 0x2a19')
			con.expect(['value:.*\n', pexpect.TIMEOUT], timeout=60)
			if con.after != pexpect.TIMEOUT: 
				batt_lvl = eval("0x" + con.after.split()[1])
				measNr += 1
				sys.stdout.write("%s Battery level: %i %% (measurement nr %i)\r" %(str(datetime.datetime.now()), batt_lvl, measNr))
				sys.stdout.flush()
				pexpect.run(send2OH %str(batt_lvl))
				time.sleep(600)
			else:
				sys.stdout.write("\n")
				connected = 0
				con.sendline('disconnect')
				con.expect('\[   \].*>', timeout=1)
	else:
		raise Exception("Unknown gatttool response: %s" %con.after)
