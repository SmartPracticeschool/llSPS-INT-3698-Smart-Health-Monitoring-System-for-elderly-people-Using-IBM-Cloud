import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "a2x11o"
deviceType = "raspberrypi"
deviceId = "1234"
authMethod = "token"
authToken = "12345678"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)#Commands
        
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        
        bpm=random.randint(20, 120)
        #print(bpm)
        temp =random.randint(30, 60)
        #Send Temperature & Bpm to IBM Watson
        data = { 'Temperature' : temp, 'Bpm': bpm }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Bpm = %s bpm" % bpm, "to IBM Watson")

        success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        if temp>38 and bpm>100:
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=4dywMeC1XqBPtSY9NgFHiLQ7xVbJEIjzUlT2aDvspk03W5AouZgtioFO03DdpSIWhbVMyR19Pxw8rfYj&sender_id=FSTSMS&message=Your health condition is critical(Temperature and bpm are abnormal!)&language=english&route=p&numbers=YOUR NUMBER')
                print(r.status_code)

                
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
