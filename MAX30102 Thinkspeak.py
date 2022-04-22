import max30102
import hrcalc
import time
m = max30102.MAX30102()

import smbus
from time import sleep
import http.client, urllib
import time
sleep = 6 # how many seconds to sleep between posts to the channel
key = 'G06TTU1I2AR3KD07'# Thingspeak channel to update

hr2 = 0
sp2 = 0

while True:
    red, ir = m.read_sequential()
    
    hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

    #print("hr detected:",hrb)
    #print("sp detected:",spb)

    if(hrb== False and spb==False):
            print('Finger not detected')
            flag=0

            params = urllib.parse.urlencode({'field3': sp2, 'field2': hr2,'key':key })
            headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = http.client.HTTPConnection("api.thingspeak.com:80")
            try:
                                    
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print (response.status, response.reason)
                data = response.read()
                conn.close()
            except:
                print ("connection failed")
    
    if( int(hr) in range(30,120)):
        if(hrb == True and hr != -999):
            hr2 = int(hr)+40
            print("Heart Rate : ",hr2)
            flag=1
        if(spb == True and sp != -999):
            sp2 = int(sp)
            print("SPO2       : ",sp2)
            flag=1
                
        

        if(flag==1):
            params = urllib.parse.urlencode({'field3': sp2, 'field2': hr2,'key':key })
            headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = http.client.HTTPConnection("api.thingspeak.com:80")
            try:
                                    
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print (response.status, response.reason)
                data = response.read()
                conn.close()
            except:
                print ("connection failed")
        if(flag==0):
            print("Uploading Failed")
    

    time.sleep(0.1)
