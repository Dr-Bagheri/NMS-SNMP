import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense


df_labeled = pd.read_csv('realistic-with-label.csv')
df_unlabeled = pd.read_csv('realistic.csv')

#exclude the datetime column
datetime_column = 'timestamp'  
df_labeled = df_labeled.drop(columns=[datetime_column])
df_unlabeled = df_unlabeled.drop(columns=[datetime_column])

#extract labels from the labeled dataset
labels = df_labeled['label']
df_labeled = df_labeled.drop(columns=['label'])

#convert labels to binary (1 for anomaly, 0 for normal)
binary_labels = labels.apply(lambda x: 1 if x in ['ddos', 'congestion', 'hardware_failure'] else 0)

#normalize the data
df_unlabeled_normalized = (df_unlabeled - df_unlabeled.mean()) / df_unlabeled.std()

#train an Autoencoder for Anomaly Detection
input_dim = df_unlabeled_normalized.shape[1]
encoding_dim = 14  

input_layer = Input(shape=(input_dim,))
encoder = Dense(encoding_dim, activation="relu")(input_layer)
encoder = Dense(int(encoding_dim / 2), activation="relu")(encoder)
encoder = Dense(int(encoding_dim / 4), activation="relu")(encoder)
decoder = Dense(int(encoding_dim / 2), activation='relu')(encoder)
decoder = Dense(encoding_dim, activation='relu')(decoder)
decoder = Dense(input_dim, activation='sigmoid')(decoder)

autoencoder = Model(inputs=input_layer, outputs=decoder)
autoencoder.compile(optimizer='adam', loss='mean_squared_error')

#train the autoencoder
autoencoder.fit(df_unlabeled_normalized, df_unlabeled_normalized, epochs=50, batch_size=32, shuffle=True, validation_split=0.2, verbose=1)

#get the reconstruction error
reconstructions = autoencoder.predict(df_unlabeled_normalized)
mse = np.mean(np.power(df_unlabeled_normalized - reconstructions, 2), axis=1)
threshold = np.percentile(mse, 95)  # Set threshold for anomaly detection
df_unlabeled['anomaly_autoencoder'] = mse > threshold

#apply DBSCAN to the unlabeled dataset
dbscan = DBSCAN(eps=0.5, min_samples=5)
df_unlabeled['anomaly_dbscan'] = dbscan.fit_predict(df_unlabeled_normalized)

#compare results with labeled data
print("Autoencoder Results:")
print(classification_report(binary_labels, df_unlabeled['anomaly_autoencoder'].astype(int)))
print(confusion_matrix(binary_labels, df_unlabeled['anomaly_autoencoder'].astype(int)))

print("\nDBSCAN Results:")
print(classification_report(binary_labels, df_unlabeled['anomaly_dbscan'].apply(lambda x: 1 if x == -1 else 0)))
print(confusion_matrix(binary_labels, df_unlabeled['anomaly_dbscan'].apply(lambda x: 1 if x == -1 else 0)))

#visualize the Results (DBSCAN)
pca = PCA(n_components=2)
pca_components = pca.fit_transform(df_unlabeled_normalized)
df_unlabeled['pca1'] = pca_components[:, 0]
df_unlabeled['pca2'] = pca_components[:, 1]


plt.figure(figsize=(10, 6))
plt.scatter(df_unlabeled['pca1'], df_unlabeled['pca2'], c=df_unlabeled['anomaly_dbscan'], cmap='coolwarm', alpha=0.6)
plt.title('DBSCAN Anomaly Detection')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster Label')
plt.show()