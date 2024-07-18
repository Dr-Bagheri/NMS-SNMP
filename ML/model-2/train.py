import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Bidirectional, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical

# Load the prepared datasets
train_data = pd.read_csv('train_data.csv')
validation_data = pd.read_csv('validation_data.csv')
test_data = pd.read_csv('test_data.csv')

# Extract features and labels
X_train = train_data.drop(columns=['label']).values
y_train = train_data['label'].values
X_validation = validation_data.drop(columns=['label']).values
y_validation = validation_data['label'].values
X_test = test_data.drop(columns=['label']).values
y_test = test_data['label'].values

# Encode labels
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_validation_encoded = label_encoder.transform(y_validation)
y_test_encoded = label_encoder.transform(y_test)

# Convert labels to categorical
y_train_categorical = to_categorical(y_train_encoded)
y_validation_categorical = to_categorical(y_validation_encoded)
y_test_categorical = to_categorical(y_test_encoded)

# Reshape input data to 3D (samples, timesteps, features)
timesteps = 1  # Since we are using each row as a timestep
X_train_reshaped = X_train.reshape((X_train.shape[0], timesteps, X_train.shape[1]))
X_validation_reshaped = X_validation.reshape((X_validation.shape[0], timesteps, X_validation.shape[1]))
X_test_reshaped = X_test.reshape((X_test.shape[0], timesteps, X_test.shape[1]))

# Build the optimized Bi-LSTM model
model = Sequential()
model.add(Bidirectional(LSTM(50, return_sequences=True, recurrent_dropout=0.2), input_shape=(timesteps, X_train.shape[1])))
model.add(Dropout(0.2))
model.add(Bidirectional(LSTM(50, return_sequences=False, recurrent_dropout=0.2)))
model.add(Dropout(0.2))
model.add(Dense(50, activation='relu'))
model.add(Dense(y_train_categorical.shape[1], activation='softmax'))

# Compile the model with a higher learning rate
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model with a smaller batch size and fewer epochs
history = model.fit(
    X_train_reshaped, y_train_categorical,
    epochs=50,
    batch_size=32,
    validation_data=(X_validation_reshaped, y_validation_categorical),
    verbose=1
)

# Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test_reshaped, y_test_categorical, verbose=0)
print(f'Test Accuracy: {test_accuracy:.4f}')

# Save the model
model.save('bilstm_anomaly_detection_model.h5')