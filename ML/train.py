import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import joblib

# Load the data
data = pd.read_csv('mock_cpu_ram_usage.csv')


scaler = MinMaxScaler()
data[['cpu_usage', 'ram_usage']] = scaler.fit_transform(data[['cpu_usage', 'ram_usage']])


X = data[['cpu_usage', 'ram_usage']]
y = data['anomaly']

model = Sequential([
    Dense(64, input_dim=X.shape[1], activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(X, y, epochs=50, batch_size=32, validation_split=0.1, verbose=1)

data['anomaly_pred'] = (model.predict(X) > 0.5).astype(int)

print(classification_report(y, data['anomaly_pred']))

# Save 
model.save('anomaly_detection_nn_model.h5')
joblib.dump(scaler, 'scaler.pkl')

print("Model and scaler saved successfully.")