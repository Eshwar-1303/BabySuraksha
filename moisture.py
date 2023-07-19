import RPi.GPIO as GPIO
import time
from pushbullet import Pushbullet
#import all
channel1 = 3
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel1, GPIO.IN)
def moisture_callback(channel1):
    if GPIO.input(channel1):
        pb = Pushbullet("o.H5gGESQCkco3YxVGzsdG21o6M03g8njv")
        print(pb.devices)
        dev = pb.get_device("Vivo Vivo 2018")
        push = dev.push_note("Alert!","Change Baby's Diaper")
        time.sleep(1)
        print("water detected")
    else:
        print("NO Water Detected!")

GPIO.add_event_detect(channel1, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel1, moisture_callback)  # assign function to GPIO PIN, Run function on change

while True:
    time.sleep(1)