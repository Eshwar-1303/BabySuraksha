from gpiozero import MCP3008
from time import sleep
import RPi.GPIO as GPIO
import time
import http.client as httplib
import urllib
from pushbullet import Pushbullet

key ="1EPX63IN172YAT79"

control = [5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10]
servo1 = 7
servo2 = 13
channel = 11
channel1 = 3
in1 = 18
in2 = 16
en = 22

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(channel, GPIO.IN)
GPIO.setup(channel1, GPIO.IN)
GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
# Set up channel number and SPI chip select device
reading = MCP3008(channel=0)

p1=GPIO.PWM(servo1,45)# 50hz frequency
p2=GPIO.PWM(servo2,45)# 50hz frequency

p1.start(0)# starting duty cycle ( it set the servo to 0 degree )
p2.start(0)# starting duty cycle ( it set the servo to 0 degree )


def callback(channel):
    if GPIO.input(channel):
        pb = Pushbullet("o.H5gGESQCkco3YxVGzsdG21o6M03g8njv")
        print(pb.devices)
        dev = pb.get_device("Vivo Vivo 2018")
        push = dev.push_note("Alert!","Baby Crying")
        time.sleep(1)
        while True:
            print("Sound Detected!")
            #p1.start(3)# starting duty cycle ( it set the servo to 0 degree )
            #p2.start(3)
            #p1.ChangeDutyCycle(3)
            #p2.ChangeDutyCycle(3)
            for x in range(11):
                p1.ChangeDutyCycle(control[x])
                p2.ChangeDutyCycle(control[x])
                time.sleep(0.06)
            for x in range(9,0,-1):
                p1.ChangeDutyCycle(control[x])
                p2.ChangeDutyCycle(control[x])
                time.sleep(0.06)
                
    else:
        print("Sound Not Detected")
        
    time.sleep(1)
        #print (x)

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=225)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

def moisture_callback(channel1):
        if GPIO.input(channel1):
                print("water detected")
        else:
                print("NO Water Detected!")

GPIO.add_event_detect(channel1, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel1, moisture_callback)  # assign function to GPIO PIN, Run function on change

while True:
    # Converts ACD voltage to temperature in Celsius
    temp_c = round((reading.value * 3.3) * 100, 2)
    # Convert Celsius degrees to Farenheit
    temp_f = round(temp_c * 1.8 + 32, 2)
    # Print both temperatures
    print('Temp: {}ºC    {}ºF'.format(temp_c, temp_f))
    
    params = urllib.parse.urlencode({'field6': temp_c, 'key':'1EPX63IN172YAT79' })

    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}

    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read()
    conn.close()
    
    if(temp_c >20):
        GPIO.output(in1,GPIO.HIGH)
        #GPIO.output(in2,GPIO.HIGH)
    else:
        GPIO.output(in1,GPIO.LOW)
        #GPIO.output(in2,GPIO.LOW)

    sleep(1)  # Wait 1.5 seconds for the next read