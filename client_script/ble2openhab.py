import pexpect
import time
import sys

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
	sys.stdout.write("Trying to connect (try nr %i)\r" %retry)
	sys.stdout.flush()
	retry += 1
	con.expect(['\[CON\].*>', pexpect.TIMEOUT], timeout=10)
	if con.after != pexpect.TIMEOUT:
		print "\nSuccessfully Connected to Bluetooth Device"

		# Read data, go back to trying to connect if it fails
		connected = 1
		while connected == 1:
			con.sendline('char-read-uuid 0x2a19')
			con.expect(['value:.*\n', pexpect.TIMEOUT], timeout=60)
			if con.after != pexpect.TIMEOUT: 
				batt_lvl = eval("0x" + con.after.split()[1])
				print "Battery level:", batt_lvl, "%"
				pexpect.run(send2OH %str(batt_lvl))
				time.sleep(60)
			else:
				connected = 0
				con.sendline('disconnect')
				con.expect('\[   \].*>', timeout=1)
