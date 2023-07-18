import socket
import paho.mqtt.client as mqtt
import os
import sys
import fcntl
import time
import json
from datetime import datetime
from sondehub.amateur import Uploader

global uploader

def UploadTelemetry(Sentence):
    global uploader
    # $$MQTT,3,15:36:14,51.95,-2.54,128,3*xxxx  

    Fields = Sentence.split(',')
    
    Callsign = Fields[0][2:]
    
    TimeAndDate = datetime.now().isoformat()
    
    Latitude = float(Fields[3])
    Longitude = float(Fields[4])
    Altitude = float(Fields[5])

    print('Uploading ' + Callsign + ',' + TimeAndDate + ',' + str(Latitude) + ',' + str(Longitude) + ',' + str(Altitude))

    uploader.add_telemetry(Callsign, TimeAndDate, Latitude, Longitude, Altitude)
        
def on_message(client, userdata, message):
    value = str(message.payload.decode("utf-8"))
    
    print("received topic   = ", message.topic)
    print("received message = ", value)
    
    # incoming/payloads/MQTT/sentence

    fields = message.topic.split('/')

    print(fields)
    
    PayloadType = fields[1]
    PayloadID = fields[2]
    
    if PayloadType == 'payloads':
        print('Received payload position')
        Field = fields[3]

        if Field == 'sentence':
            print(value)
            UploadTelemetry(value)
         

def RunLoop():
    global uploader
    
    if len(sys.argv) < 4:
        print ("Usage: python mqtt_sondehub.py <gateway_callsign> <mqtt_broker> <mqtt_path> [<mqtt_username> <mqtt_password>]")
        quit()

    uploader = Uploader(sys.argv[1])
      
    mqttc = mqtt.Client("sondehub_gateway")
    
    if len(sys.argv) > 5:
        mqttc.username_pw_set(sys.argv[4], sys.argv[5]) 
        
    mqttc.on_message=on_message

    print("Connecting to mqtt broker " + sys.argv[2])
    
    mqttc.connect(sys.argv[2], 1883)
    mqttc.loop_start()
    
    print("Connected to mqtt broker " + sys.argv[2])
    
    mqttc.subscribe(sys.argv[3], qos=0)
    
    print("Subscribed to " + sys.argv[3])

    while True:
        time.sleep(1)
            
def run_once():
    global fh
    fh=open(os.path.realpath(__file__),'r')
    # try:
    fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
    RunLoop()
    # except:
        # print("Already Running!!")
        # os._exit(0)

run_once()
        


