import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix
from keras.models import Model, Sequential
from keras.layers import Input, Dense
import matplotlib.pyplot as plt


df_labeled = pd.read_csv('realistic-with-label_new.csv')
df_unlabeled = pd.read_csv('realistic_new.csv')

#exclude the datetime column
datetime_column = 'timestamp'
df_labeled = df_labeled.drop(columns=[datetime_column])
df_unlabeled = df_unlabeled.drop(columns=[datetime_column])

#extract labels from the labeled dataset
labels = df_labeled['label']
df_labeled = df_labeled.drop(columns=['label'])

#normalize the data
scaler = MinMaxScaler()
df_labeled_scaled = scaler.fit_transform(df_labeled)
df_unlabeled_scaled = scaler.transform(df_unlabeled)

#define the autoencoder model
input_dim = df_labeled_scaled.shape[1]
encoding_dim = 14  # Number of neurons in the encoding layer

input_layer = Input(shape=(input_dim,))
encoder = Dense(encoding_dim, activation="relu")(input_layer)
decoder = Dense(input_dim, activation="sigmoid")(encoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)
autoencoder.compile(optimizer='adam', loss='mse')
autoencoder.summary()

#train the autoencoder
autoencoder.fit(df_labeled_scaled, df_labeled_scaled, epochs=50, batch_size=32, validation_split=0.2)

#predict the reconstruction for the unlabeled dataset
reconstructions = autoencoder.predict(df_unlabeled_scaled)

#calculate the reconstruction errors
reconstruction_errors = np.mean(np.square(df_unlabeled_scaled - reconstructions), axis=1)

#define the anomaly threshold
threshold = np.percentile(reconstruction_errors, 95)

#detect anomalies
anomalies = reconstruction_errors > threshold

#convert labels to binary (1 for anomaly, 0 for normal)
binary_labels = labels.apply(lambda x: 1 if x in ['ddos', 'congestion', 'hardware_failure'] else 0)

#visualize the results
plt.figure(figsize=(10, 6))
plt.scatter(range(len(reconstruction_errors)), reconstruction_errors, c=anomalies, cmap='coolwarm', alpha=0.6, marker='o')
plt.axhline(y=threshold, color='r', linestyle='--', label='Anomaly Threshold')
plt.title('Autoencoder Anomaly Detection')
plt.xlabel('Data Point Index')
plt.ylabel('Reconstruction Error')
plt.legend()
plt.savefig('autoencoder_anomaly_detection.png')

print("\nAutoencoder Results:")
print(classification_report(binary_labels[:len(anomalies)], anomalies))
print(confusion_matrix(binary_labels[:len(anomalies)], anomalies))