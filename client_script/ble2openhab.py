from bluepy import btle
import struct
import pexpect
import datetime
import time

send2OH = 'curl --header "Content-Type: text/plain" --request PUT --data "%s" http://192.168.0.6:8080/rest/items/%s/state'
# Timeout in minutes
timeout = 1.0/6

def listAll(p):
	for svc in p.getServices():
		print(svc.uuid.getCommonName())
		for ch in svc.getCharacteristics():
			print(" " + str(ch.valHandle) + ": " + ch.uuid.getCommonName())
def getBatLvl(p):
	svc = p.getServiceByUUID( "180F" )
	chBat = svc.getCharacteristics()[0]
	batVal = struct.unpack('b', chBat.read())[0]
	pexpect.run(send2OH %(str(batVal), "Battery_Level"))
	print(batVal)

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        #print("A notification was received: " + data + "<-- data")
	#print(cHandle)

	# Get battery level
        getBatLvl(self)


p = btle.Peripheral("f2:5c:dc:a2:94:ea", btle.ADDR_TYPE_RANDOM)
p.setDelegate( MyDelegate() )

listAll(p)

# Setup to turn notifications on, e.g.
#svc = p.getServiceByUUID( "e198000158b346e7b9a6bedfad46833c" )
#ch = svc.getCharacteristics()[0]

#print(ch.valHandle)

#p.writeCharacteristic(ch.valHandle+1, "\x02\x00")
#
#while True:
#    if p.waitForNotifications(int(timeout*60)):
#        # handleNotification() was called
#        continue
#
#    print(str(datetime.datetime.now()).split('.')[0] + ": Waited for %i min without notification..." %(timeout))
#    # Perhaps do something else here

while True:
   getBatLvl(p) 
   time.sleep(int(timeout*60))
