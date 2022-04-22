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

#---------------------------------------------
def read_temp():
    class MLX90614():

        MLX90614_RAWIR1=0x04
        MLX90614_RAWIR2=0x05
        MLX90614_TA=0x06
        MLX90614_TOBJ1=0x07
        MLX90614_TOBJ2=0x08

        MLX90614_TOMAX=0x20
        MLX90614_TOMIN=0x21
        MLX90614_PWMCTRL=0x22
        MLX90614_TARANGE=0x23
        MLX90614_EMISS=0x24
        MLX90614_CONFIG=0x25
        MLX90614_ADDR=0x0E
        MLX90614_ID1=0x3C
        MLX90614_ID2=0x3D
        MLX90614_ID3=0x3E
        MLX90614_ID4=0x3F

        comm_retries = 5
        comm_sleep_amount = 0.1

        def __init__(self, address=0x5a, bus_num=1):
            self.bus_num = bus_num
            self.address = address
            self.bus = smbus.SMBus(bus=bus_num)

        def read_reg(self, reg_addr):
            err = None
            for i in range(self.comm_retries):
                try:
                    return self.bus.read_word_data(self.address, reg_addr)
                except IOError as e:
                    err = e
                    #"Rate limiting" - sleeping to prevent problems with sensor
                    #when requesting data too quickly
                    sleep(self.comm_sleep_amount)
            #By this time, we made a couple requests and the sensor didn't respond
            #(judging by the fact we haven't returned from this function yet)
            #So let's just re-raise the last IOError we got
            raise err
        def data_to_temp(self, data):
            temp = (data*0.02) - 273.15
            return temp

        def get_amb_temp(self):
            data = self.read_reg(self.MLX90614_TA)
            return self.data_to_temp(data)

        def get_obj_temp(self):
            data = self.read_reg(self.MLX90614_TOBJ1)
            return self.data_to_temp(data)


    if __name__ == "__main__":
        sensor = MLX90614()
        #print("Ambient Temp:", sensor.get_amb_temp())
        #print("Object Temp:", sensor.get_obj_temp())
       
    return sensor.get_obj_temp()
    

#--------------------------------------------

while True:
    
    red, ir = m.read_sequential()
    
    hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

    temp=read_temp();

    #print("hr detected:",hrb)
    #print("sp detected:",spb)

    if(hrb== False and spb==False):
            print('Finger not detected')
            
            flag=0
            print("Object Temp:", temp)

            params = urllib.parse.urlencode({'field1': temp, 'field3': sp2, 'field2': hr2,'key':key })
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
    
    if( int(hr) in range(30,110)):
        if(hrb == True and hr != -999):
            hr2 = int(hr)+40
            print("Heart Rate : ",hr2)
            flag=1
        if(spb == True and sp != -999):
            sp2 = int(sp)
            print("SPO2       : ",sp2)
            flag=1
                
        print("Object Temp:", temp)

        if(flag==1):
            params = urllib.parse.urlencode({'field1': temp, 'field3': sp2, 'field2': hr2,'key':key })
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
