import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LayerNormalization, Dropout, MultiHeadAttention, Conv1D, GlobalAveragePooling1D, Add, Embedding, Bidirectional, LSTM, Flatten
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

# Define the Conformer block
def conformer_block(inputs, num_heads, ff_dim, conv_kernel_size=32, dropout=0.1):
    # Multi-Head Self Attention
    x = LayerNormalization(epsilon=1e-6)(inputs)
    x = MultiHeadAttention(num_heads=num_heads, key_dim=ff_dim, dropout=dropout)(x, x)
    x = Dropout(dropout)(x)
    x = Add()([inputs, x])

    # Convolution Module
    y = LayerNormalization(epsilon=1e-6)(x)
    y = Conv1D(filters=ff_dim, kernel_size=conv_kernel_size, padding='same', activation='relu')(y)
    y = Dropout(dropout)(y)
    y = Conv1D(filters=inputs.shape[-1], kernel_size=conv_kernel_size, padding='same')(y)
    y = Dropout(dropout)(y)
    y = Add()([x, y])

    # Feed Forward Module
    z = LayerNormalization(epsilon=1e-6)(y)
    z = Dense(ff_dim, activation='relu')(z)
    z = Dropout(dropout)(z)
    z = Dense(inputs.shape[-1])(z)
    z = Dropout(dropout)(z)
    return Add()([y, z])

# Define the hybrid model
input_shape = (timesteps, X_train.shape[1])
inputs = Input(shape=input_shape)

# Embedding layer
x = Dense(128, activation='relu')(inputs)

# Bi-LSTM layer
x = Bidirectional(LSTM(64, return_sequences=True, recurrent_dropout=0.2))(x)

# Conformer block
x = conformer_block(x, num_heads=4, ff_dim=64)

# Flatten and output layer
x = Flatten()(x)
x = Dense(50, activation='relu')(x)
x = Dropout(0.1)(x)
outputs = Dense(y_train_categorical.shape[1], activation='softmax')(x)

model = Model(inputs, outputs)

# Compile the model
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
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
model.save('bilstm_conformer_anomaly_detection_model.h5')