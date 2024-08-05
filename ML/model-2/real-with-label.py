import pandas as pd
import numpy as np

df_anomalous = pd.read_csv('anomalous_snmp_data.csv')



#add random noise
def add_noise(data, noise_level=0.1):
    noise = np.random.normal(0, noise_level, data.shape)
    return data + noise

#gradual changes
def introduce_gradual_change(data, change_factor=0.05):
    gradual_change = np.linspace(1, 1 + change_factor, num=len(data))
    return data * gradual_change

#combine multiple features to create complex anomalies
def combine_features(data, columns, weight=0.5):
    combined = data[columns[0]] * weight + data[columns[1]] * (1 - weight)
    return combined

#apply random multipliers
def apply_random_multiplier(data, min_factor=1.5, max_factor=10):
    multiplier = np.random.uniform(min_factor, max_factor, size=data.shape)
    return data * multiplier


label_column = 'label'  
for column in df_anomalous.columns:
    if column != label_column and pd.api.types.is_numeric_dtype(df_anomalous[column]):  # Skip the label column and ensure the column is numeric
        #add random noise to the anomalies
        df_anomalous.loc[df_anomalous[label_column] == 'ddos', column] = add_noise(df_anomalous.loc[df_anomalous[label_column] == 'ddos', column])
        df_anomalous.loc[df_anomalous[label_column] == 'congestion', column] = add_noise(df_anomalous.loc[df_anomalous[label_column] == 'congestion', column])
        df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column] = add_noise(df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column])
        
        #introduce gradual changes to the anomalies
        df_anomalous.loc[df_anomalous[label_column] == 'ddos', column] = introduce_gradual_change(df_anomalous.loc[df_anomalous[label_column] == 'ddos', column])
        df_anomalous.loc[df_anomalous[label_column] == 'congestion', column] = introduce_gradual_change(df_anomalous.loc[df_anomalous[label_column] == 'congestion', column])
        df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column] = introduce_gradual_change(df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column])
        
        #combine multiple features to create complex anomalies
        if column in ['ifInOctets', 'ifOutOctets']:  #example columns to combine
            df_anomalous.loc[df_anomalous[label_column] == 'ddos', column] = combine_features(df_anomalous, ['ifInOctets', 'ifOutOctets'])
            df_anomalous.loc[df_anomalous[label_column] == 'congestion', column] = combine_features(df_anomalous, ['ifInOctets', 'ifOutOctets'])
            df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column] = combine_features(df_anomalous, ['ifInOctets', 'ifOutOctets'])
        
        #apply random multipliers to the anomalies
        df_anomalous.loc[df_anomalous[label_column] == 'ddos', column] = apply_random_multiplier(df_anomalous.loc[df_anomalous[label_column] == 'ddos', column])
        df_anomalous.loc[df_anomalous[label_column] == 'congestion', column] = apply_random_multiplier(df_anomalous.loc[df_anomalous[label_column] == 'congestion', column])
        df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column] = apply_random_multiplier(df_anomalous.loc[df_anomalous[label_column] == 'hardware_failure', column])





df_anomalous.to_csv('realistic-with-label.csv', index=False)