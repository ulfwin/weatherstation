from bluepy.btle import Peripheral

class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data)
        print("A notification was received")


device = Peripheral("f2:5c:dc:a2:94:ea", btle.ADDR_TYPE_RANDOM)
