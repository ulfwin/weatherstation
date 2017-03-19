from bluepy import btle

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("A notification was received: ", data, "<-- data")
	print(cHandle)


p = btle.Peripheral("f2:5c:dc:a2:94:ea", btle.ADDR_TYPE_RANDOM)
p.setDelegate( MyDelegate() )

# Setup to turn notifications on, e.g.
svc = p.getServiceByUUID( "e198000258b346e7b9a6bedfad46833c" )
ch = svc.getCharacteristics()[0]
print(ch.valHandle)

p.writeCharacteristic(ch.valHandle+1, "\x02\x00")

while True:
    if p.waitForNotifications(600):
        # handleNotification() was called
        continue

    print("Waited for 10 min without notification...")
    # Perhaps do something else here
