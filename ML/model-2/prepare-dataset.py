from sklearn.preprocessing import StandardScaler
import pandas as pd


df_anomalous = pd.read_csv('anomalous_snmp_data.csv')


features = [
    'ifInOctets', 'ifOutOctets', 'ipInReceives', 'ipOutRequests', 'tcpInSegs', 'tcpOutSegs',
    'udpInDatagrams', 'udpOutDatagrams', 'ifInDiscards', 'ifOutDiscards', 'ifInErrors', 'ifOutErrors',
    'ifSpeed', 'sysUpTime', 'ifOperStatus', 'ifLastChange', 'hrProcessorLoad', 'hrMemorySize', 'hrStorageUsed'
]


X = df_anomalous[features]
y = df_anomalous['label']


train_split_index = int(0.7 * len(df_anomalous))
validation_split_index = int(0.85 * len(df_anomalous))


X_train = X[:train_split_index]
y_train = y[:train_split_index]
X_validation = X[train_split_index:validation_split_index]
y_validation = y[train_split_index:validation_split_index]
X_test = X[validation_split_index:]
y_test = y[validation_split_index:]

# Normalize the data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_validation_scaled = scaler.transform(X_validation)
X_test_scaled = scaler.transform(X_test)

# Save the prepared dataset
train_data = pd.DataFrame(X_train_scaled, columns=features)
train_data['label'] = y_train.values
validation_data = pd.DataFrame(X_validation_scaled, columns=features)
validation_data['label'] = y_validation.values
test_data = pd.DataFrame(X_test_scaled, columns=features)
test_data['label'] = y_test.values

train_data.to_csv('train_data.csv', index=False)
validation_data.to_csv('validation_data.csv', index=False)
test_data.to_csv('test_data.csv', index=False)