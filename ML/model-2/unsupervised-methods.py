import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


df_anomalous = pd.read_csv('realistic.csv')


datetime_column = 'timestamp'  #replace with the actual name of the datetime column
df_anomalous = df_anomalous.drop(columns=[datetime_column])

#apply IF
iso_forest = IsolationForest(contamination=0.01, random_state=42)
df_anomalous['anomaly_iso'] = iso_forest.fit_predict(df_anomalous)

#apply DBSCAN
dbscan = DBSCAN(eps=0.5, min_samples=5)
df_anomalous['anomaly_dbscan'] = dbscan.fit_predict(df_anomalous)


pca = PCA(n_components=2)
pca_components = pca.fit_transform(df_anomalous.drop(columns=['anomaly_iso', 'anomaly_dbscan']))
df_anomalous['pca1'] = pca_components[:, 0]
df_anomalous['pca2'] = pca_components[:, 1]


plt.figure(figsize=(10, 6))
plt.scatter(df_anomalous['pca1'], df_anomalous['pca2'], c=df_anomalous['anomaly_dbscan'], cmap='coolwarm', alpha=0.6)
plt.title('DBSCAN Anomaly Detection')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster Label')
plt.show()

#display the first few rows with anomaly labels
print(df_anomalous.head())