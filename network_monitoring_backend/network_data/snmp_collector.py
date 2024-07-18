import random
import requests
from datetime import datetime, timedelta
from pysnmp.hlapi import *  
import time
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from keras.models import load_model
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional

# Load the trained BI-LSTM model
model = load_model('bilstm_anomaly_detection_model.h5')
scaler = joblib.load('scaler.pkl')

def send_to_ws(data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)('snmp', {'type': 'send.snmp.data', 'message': data})

def fetch_snmp_data(target_ip, oid, test_mode=True):
    if test_mode:
        return None
    else:
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
                return varBind[1].prettyPrint()


def collect_snmp_data():
    device_ip = '192.168.1.1' 
    cpu_usage_oid = 'cpu'  
    ram_usage_oid = 'ram'  

    test_mode = True  # Set to True for testing with mock data

    if test_mode:
    
        timestamp = datetime.now().isoformat()
        data = {
            'timestamp': timestamp,
            'ifInOctets': np.random.normal(loc=1000, scale=100),
            'ifOutOctets': np.random.normal(loc=1000, scale=100),
            'ipInReceives': np.random.normal(loc=500, scale=50),
            'ipOutRequests': np.random.normal(loc=500, scale=50),
            'tcpInSegs': np.random.normal(loc=300, scale=30),
            'tcpOutSegs': np.random.normal(loc=300, scale=30),
            'udpInDatagrams': np.random.normal(loc=200, scale=20),
            'udpOutDatagrams': np.random.normal(loc=200, scale=20),
            'ifInDiscards': np.random.normal(loc=10, scale=2),
            'ifOutDiscards': np.random.normal(loc=10, scale=2),
            'ifInErrors': np.random.normal(loc=5, scale=1),
            'ifOutErrors': np.random.normal(loc=5, scale=1),
            'ifSpeed': np.random.normal(loc=10000, scale=500),
            'sysUpTime': np.random.normal(loc=100000, scale=1000),
            'ifOperStatus': np.random.choice([1, 2], p=[0.99, 0.01]),
            'ifLastChange': np.random.normal(loc=1000, scale=100),
            'hrProcessorLoad': np.random.normal(loc=50, scale=10),
            'hrMemorySize': np.random.normal(loc=16000, scale=500),
            'hrStorageUsed': np.random.normal(loc=50, scale=10)
        }
        return data

# Function to mock normal SNMP data
def mock_normal_data(duration_seconds):
    end_time = datetime.now() + timedelta(seconds=duration_seconds)
    data = []
    while datetime.now() < end_time:
        data.append(collect_snmp_data())
        time.sleep(1)  # Collect data every 1 second
    return pd.DataFrame(data)

# Function to inject anomalies
def inject_anomalies(df):
    anomaly_type = random.choice(['ddos', 'congestion', 'hardware_failure'])
    start_idx = random.randint(0, len(df) - 20)
    duration = random.randint(10, 20)
    
    if anomaly_type == 'ddos':
        df.loc[start_idx:start_idx + duration, ['ifInOctets', 'ipInReceives', 'tcpInSegs']] *= 10
    elif anomaly_type == 'congestion':
        df.loc[start_idx:start_idx + duration, ['ifInDiscards', 'ifOutDiscards', 'ifInErrors']] *= 5
    elif anomaly_type == 'hardware_failure':
        df.loc[start_idx:start_idx + duration, 'ifOperStatus'] = 2
        df.loc[start_idx:start_idx + duration, 'ifOutErrors'] *= 5
    
    return df, anomaly_type

# Function to collect or mock data and inject anomalies
def collect_or_mock_data(duration_seconds=60):
    try:
        data = mock_normal_data(duration_seconds)
    except:
        data = mock_normal_data(duration_seconds)
    
    data, anomaly_type = inject_anomalies(data)
    return data, anomaly_type

# Function to preprocess data for the model
def preprocess_data(df):
    features = [
        'ifInOctets', 'ifOutOctets', 'ipInReceives', 'ipOutRequests', 'tcpInSegs', 'tcpOutSegs',
        'udpInDatagrams', 'udpOutDatagrams', 'ifInDiscards', 'ifOutDiscards', 'ifInErrors', 'ifOutErrors',
        'ifSpeed', 'sysUpTime', 'ifOperStatus', 'ifLastChange', 'hrProcessorLoad', 'hrMemorySize', 'hrStorageUsed'
    ]
    X = df[features].values
    X_reshaped = X.reshape((X.shape[0], 1, X.shape[1]))
    return X_reshaped

# Function to make predictions
def make_predictions(df):
    X_reshaped = preprocess_data(df)
    predictions = model.predict(X_reshaped)
    predicted_labels = np.argmax(predictions, axis=1)  # Get the index of the highest probability class
    return predicted_labels

# Main function to run the anomaly detection
def run_anomaly_detection():
    data, anomaly_type = collect_or_mock_data()
    predicted_labels = make_predictions(data)
    for i, row in data.iterrows():
        row['anomaly_type'] = anomaly_type
        row['predicted_label'] = predicted_labels[i]  # Assign the predicted label
        url = 'http://localhost:8000/api/data/'
        response = requests.post(url, json=row.to_dict())  # Sending as JSON
        send_to_ws(row.to_dict())
        if response.status_code == 201:
            print("Data successfully posted.")
        else:
            print(f"Failed to post data: {response.status_code}, {response.text}")

