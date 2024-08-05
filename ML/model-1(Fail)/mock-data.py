import pandas as pd
import numpy as np


np.random.seed(42)


num_points = 100000


cpu_usage = np.random.uniform(10, 80, num_points)
ram_usage = np.random.uniform(10, 80, num_points)


data = pd.DataFrame({
    'cpu_usage': cpu_usage,
    'ram_usage': ram_usage
})


def inject_anomalies(data, num_anomalies):
    anomalies = []
    for _ in range(num_anomalies):
        anomaly_type = np.random.choice(['cpu_high_ram_low', 'ram_high_cpu_low', 'both_high'])
        if anomaly_type == 'cpu_high_ram_low':
            cpu = np.random.uniform(90, 100)
            ram = np.random.uniform(0, 20)
        elif anomaly_type == 'ram_high_cpu_low':
            cpu = np.random.uniform(0, 20)
            ram = np.random.uniform(90, 100)
        elif anomaly_type == 'both_high':
            cpu = np.random.uniform(90, 100)
            ram = np.random.uniform(90, 100)
        anomalies.append([cpu, ram])
    return anomalies


num_anomalies = 30000


anomalies = inject_anomalies(data, num_anomalies)
anomalies_df = pd.DataFrame(anomalies, columns=['cpu_usage', 'ram_usage'])


data = pd.concat([data, anomalies_df], ignore_index=True)


data = data.sample(frac=1).reset_index(drop=True)


def label_anomalies(row):
    if (90 <= row['cpu_usage'] <= 100 and row['ram_usage'] < 20) or \
       (90 <= row['ram_usage'] <= 100 and row['cpu_usage'] < 20) or \
       (row['cpu_usage'] > 90 and row['ram_usage'] > 90):
        return 1
    else:
        return 0

data['anomaly'] = data.apply(label_anomalies, axis=1)


data.to_csv('mock_cpu_ram_usage.csv', index=False)
#test