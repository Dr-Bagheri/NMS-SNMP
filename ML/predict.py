import numpy as np
from keras.models import load_model
import joblib


model = load_model('anomaly_detection_nn_model.h5')
scaler = joblib.load('scaler.pkl')


def predict_anomaly(cpu_usage, ram_usage):

    input_data = scaler.transform([[cpu_usage, ram_usage]])

    prediction = model.predict(input_data)
    return 1 if prediction > 0.5 else 0

# Example
cpu_usage = 80
ram_usage = 80
is_anomaly = predict_anomaly(cpu_usage, ram_usage)
print(f"Anomaly: {is_anomaly}")