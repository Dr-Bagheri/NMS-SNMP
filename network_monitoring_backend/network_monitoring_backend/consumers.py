import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from keras.models import load_model
import joblib

# Load the anomaly detection model and scaler
model = load_model('anomaly_detection_nn_model.h5')
scaler = joblib.load('scaler.pkl')

class SNMPConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.channel_layer = get_channel_layer()
        async_to_sync(self.channel_layer.group_add)("snmp", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("snmp", self.channel_name)

    def receive(self, text_data):
        data = json.loads(text_data)
        cpu_usage = data.get('cpu_usage')
        ram_usage = data.get('ram_usage')

        if cpu_usage is not None and ram_usage is not None:
            # Normalize the input
            input_data = scaler.transform([[cpu_usage, ram_usage]])
            # Predict anomaly
            prediction = model.predict(input_data)
            is_anomaly = 1 if prediction > 0.5 else 0
            self.send(text_data=json.dumps({
                'cpu_usage': cpu_usage,
                'ram_usage': ram_usage,
                'anomaly': is_anomaly
            }))
        else:
            # Process SNMP data
            self.send(text_data=json.dumps({
                'message': 'SNMP data received'
            }))

    def send_snmp_data(self, event):
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))