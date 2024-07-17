import random
import pandas as pd


df_normal = pd.read_csv('normal_snmp_data.csv')


def inject_ddos(df, start_idx, duration):
    end_idx = start_idx + duration
    df.loc[start_idx:end_idx, 'ifInOctets'] *= 10
    df.loc[start_idx:end_idx, 'ipInReceives'] *= 10
    df.loc[start_idx:end_idx, 'tcpInSegs'] *= 10
    return df


def inject_congestion(df, start_idx, duration):
    end_idx = start_idx + duration
    df.loc[start_idx:end_idx, 'ifInDiscards'] *= 5
    df.loc[start_idx:end_idx, 'ifOutDiscards'] *= 5
    df.loc[start_idx:end_idx, 'ifInErrors'] *= 5
    return df


def inject_hardware_failure(df, start_idx, duration):
    end_idx = start_idx + duration
    df.loc[start_idx:end_idx, 'ifOperStatus'] = 2
    df.loc[start_idx:end_idx, 'ifOutErrors'] *= 5
    return df

# Inject anomalies
num_points = len(df_normal)
anomaly_duration = 12 * 60 * 5  # 1 hour duration (12*60*5 seconds)
num_anomalies = int(0.3 * num_points / anomaly_duration)  # Number of anomalies needed to cover 30% of the dataset

# Randomly select start points for anomalies
anomaly_starts = random.sample(range(0, num_points - anomaly_duration), num_anomalies * 3)

# Inject anomalies into the dataset
df_anomalous = df_normal.copy()
labels = ['ddos', 'congestion', 'hardware_failure']

for i in range(num_anomalies):
    ddos_start = anomaly_starts[i * 3]
    congestion_start = anomaly_starts[i * 3 + 1]
    hardware_failure_start = anomaly_starts[i * 3 + 2]
    
    df_anomalous = inject_ddos(df_anomalous, ddos_start, anomaly_duration)
    df_anomalous = inject_congestion(df_anomalous, congestion_start, anomaly_duration)
    df_anomalous = inject_hardware_failure(df_anomalous, hardware_failure_start, anomaly_duration)
    
    df_anomalous.loc[ddos_start:ddos_start + anomaly_duration, 'label'] = 'ddos'
    df_anomalous.loc[congestion_start:congestion_start + anomaly_duration, 'label'] = 'congestion'
    df_anomalous.loc[hardware_failure_start:hardware_failure_start + anomaly_duration, 'label'] = 'hardware_failure'


df_anomalous['label'].fillna('normal', inplace=True)
df_anomalous.to_csv('/mnt/data/anomalous_snmp_data_temporal.csv', index=False)