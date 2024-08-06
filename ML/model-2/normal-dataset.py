import pandas as pd
import numpy as np


date_range = pd.date_range(start='2023-01-01', end='2023-01-31 23:59:55', freq='5S')
num_points = len(date_range)

data = {
    'timestamp': date_range,
    'ifInOctets': np.random.normal(loc=1000, scale=100, size=num_points),
    'ifOutOctets': np.random.normal(loc=1000, scale=100, size=num_points),
    'ipInReceives': np.random.normal(loc=500, scale=50, size=num_points),
    'ipOutRequests': np.random.normal(loc=500, scale=50, size=num_points),
    'tcpInSegs': np.random.normal(loc=300, scale=30, size=num_points),
    'tcpOutSegs': np.random.normal(loc=300, scale=30, size=num_points),
    'udpInDatagrams': np.random.normal(loc=200, scale=20, size=num_points),
    'udpOutDatagrams': np.random.normal(loc=200, scale=20, size=num_points),
    'ifInDiscards': np.random.normal(loc=10, scale=2, size=num_points),
    'ifOutDiscards': np.random.normal(loc=10, scale=2, size=num_points),
    'ifInErrors': np.random.normal(loc=5, scale=1, size=num_points),
    'ifOutErrors': np.random.normal(loc=5, scale=1, size=num_points),
    'ifSpeed': np.random.normal(loc=10000, scale=500, size=num_points),
    'sysUpTime': np.linspace(0, num_points*5, num_points),  
    'ifOperStatus': np.random.choice([1, 2], size=num_points, p=[0.99, 0.01]), 
    'ifLastChange': np.random.normal(loc=1000, scale=100, size=num_points),
    'hrProcessorLoad': np.random.normal(loc=20, scale=5, size=num_points),
    'hrMemorySize': np.random.normal(loc=16000, scale=500, size=num_points),
    'hrStorageUsed': np.random.normal(loc=8000, scale=300, size=num_points)
}


df_normal = pd.DataFrame(data)
df_normal.to_csv('normal_snmp_data_new.csv', index=False)