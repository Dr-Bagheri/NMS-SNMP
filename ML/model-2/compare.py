import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


df_labeled = pd.read_csv('realistic-with-label.csv')
df_unlabeled = pd.read_csv('realistic.csv')


#exclude the datetime column
datetime_column = 'timestamp'  
df_labeled = df_labeled.drop(columns=[datetime_column])
df_unlabeled = df_unlabeled.drop(columns=[datetime_column])

#extract labels from the labeled dataset
labels = df_labeled['label']
df_labeled = df_labeled.drop(columns=['label'])

#apply Isolation Forest to the unlabeled dataset
iso_forest = IsolationForest(contamination=0.01, random_state=42)
df_unlabeled['anomaly_iso'] = iso_forest.fit_predict(df_unlabeled)

#apply DBSCAN to the unlabeled dataset
dbscan = DBSCAN(eps=0.5, min_samples=5)
df_unlabeled['anomaly_dbscan'] = dbscan.fit_predict(df_unlabeled)

#convert labels to binary (1 for anomaly, 0 for normal)
binary_labels = labels.apply(lambda x: 1 if x in ['ddos', 'congestion', 'hardware_failure'] else 0)

#compare results with labeled data
print("Isolation Forest Results:")
print(classification_report(binary_labels, df_unlabeled['anomaly_iso'].apply(lambda x: 1 if x == -1 else 0)))
print(confusion_matrix(binary_labels, df_unlabeled['anomaly_iso'].apply(lambda x: 1 if x == -1 else 0)))

print("\nDBSCAN Results:")
print(classification_report(binary_labels, df_unlabeled['anomaly_dbscan'].apply(lambda x: 1 if x == -1 else 0)))
print(confusion_matrix(binary_labels, df_unlabeled['anomaly_dbscan'].apply(lambda x: 1 if x == -1 else 0)))

#visualize the results (DBSCAN)
pca = PCA(n_components=2)
pca_components = pca.fit_transform(df_unlabeled.drop(columns=['anomaly_iso', 'anomaly_dbscan']))
df_unlabeled['pca1'] = pca_components[:, 0]
df_unlabeled['pca2'] = pca_components[:, 1]


plt.figure(figsize=(10, 6))
plt.scatter(df_unlabeled['pca1'], df_unlabeled['pca2'], c=df_unlabeled['anomaly_dbscan'], cmap='coolwarm', alpha=0.6)
plt.title('DBSCAN Anomaly Detection')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster Label')
plt.show()