import pexpect
#import random
import time

gatttool_cmd = 'gatttool -b DD:4F:3B:2C:A0:5B -I'
send2OH = 'curl --header "Content-Type: text/plain" --request PUT --data "%s" http://localhost:8080/rest/items/Battery_Level/state'

#temp = int(20 + 10*random.random())
con = pexpect.spawn(gatttool_cmd)
con.expect('\[LE\]>', timeout=1)
con.sendline('connect')
con.expect('\[CON\].*>', timeout=1)
while 1:
	con.sendline('char-read-uuid 0x2a19')
	con.expect('value:.*\n', timeout=1)
	#print eval("0x" + con.after.split()[1]), "%"
	batt_lvl = eval("0x" + con.after.split()[1])
	pexpect.run(send2OH %str(batt_lvl))
	time.sleep(10)
