import pexpect
import time

gatttool_cmd = 'gatttool -b DD:4F:3B:2C:A0:5B -I'
con = pexpect.spawn(gatttool_cmd)
con.expect('\[LE\]>', timeout=1)
con.sendline('connect')
con.expect('\[CON\].*>', timeout=1)
while 1:
	con.sendline('char-read-uuid 0x2a19')
	con.expect('value:.*\n', timeout=1)
	print eval("0x" + con.after.split()[1]), "%"
	time.sleep(1)
