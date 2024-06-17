import random
import requests
from datetime import datetime
from pysnmp.hlapi import *  
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from keras.models import load_model
import joblib


model = load_model('anomaly_detection_nn_model.h5')
scaler = joblib.load('scaler.pkl')

def send_to_ws(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('snmp', {'type': 'send.snmp.data', 'message': data})

    
def fetch_snmp_data(target_ip, oid, test_mode=True):
    if test_mode:
        #print(f"Fetching SNMP test data for {target_ip} with OID: {oid}")
        # Mocking different response...

        if "cpu" in oid:
            simulated_value = round(random.uniform(5, 99), 2)
            #print(f"Simulated CPU usage: {simulated_value}")
            return simulated_value
        elif "ram" in oid:
            simulated_value = round(random.uniform(5, 99), 2)
            #print(f"Simulated RAM usage: {simulated_value}")
            return simulated_value
        else:
            print(f"No matching condition for OID: {oid}. Returning None.")
            return None
    else:
        print(f"Fetching SNMP data for {target_ip} with OID: {oid}")
        iterator = getCmd(
            SnmpEngine(),
            CommunityData('public'), 
            UdpTransportTarget((target_ip, 161)),  # Using standard SNMP port 161
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        error_indication, error_status, error_index, result = next(iterator)

        if error_indication:
            print(error_indication)
            return None
        elif error_status:
            print(f"{error_status.prettyPrint()} at {error_index and result[int(error_index) - 1][0] or '?'}")
            return None
        else:
            for varBind in result:
                # Returns SNMP OID and its corresponding value
                return varBind[1].prettyPrint()


def collect_snmp_data():

    device_ip = '192.168.1.1' 
    cpu_usage_oid = 'cpu'  
    ram_usage_oid = 'ram'  

    test_mode = True  # Set to True for testing with mock data

    cpu_usage = fetch_snmp_data(device_ip, cpu_usage_oid, test_mode)
    ram_usage = fetch_snmp_data(device_ip, ram_usage_oid, test_mode)

    # Ensure values are not None before attempting to post
    if cpu_usage is None or ram_usage is None:
        print("Failed to fetch SNMP data.")
    
    else:
        timestamp = datetime.now().isoformat()
        # Normalize the input
        input_data = scaler.transform([[cpu_usage, ram_usage]])
        # Predict anomaly
        prediction = model.predict(input_data)
        is_anomaly = 1 if prediction > 0.5 else 0
        
        
        data = {
            "device_name": "Device1" if test_mode else device_ip,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "timestamp": timestamp, 
            "anomaly": is_anomaly,            
        }


        url = 'http://localhost:8000/api/data/'
        response = requests.post(url, json=data)  # Sending as JSON
        send_to_ws({
            "device_name": "Device1" if test_mode else device_ip,
            "cpu_usage": cpu_usage,
            "ram_usage": ram_usage,
            "timestamp": timestamp,
            "anomaly": is_anomaly,            
        })
        
        if response.status_code == 201:
            print("Data successfully posted.")
        else:
            print(f"Failed to post data: {response.status_code}, {response.text}")
    #print("Collecting SNMP data...")
    time.sleep(1)