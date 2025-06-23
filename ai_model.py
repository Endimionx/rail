
import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator

def predict_next(draws):
    if len(draws) < 5:
        return None, []

    X_data = np.array(draws).reshape(-1, 1) / 9999.0
    gen = TimeseriesGenerator(X_data, X_data, length=3, batch_size=1)

    model = Sequential([
        LSTM(32, activation='relu', input_shape=(3, 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    model.fit(gen, epochs=500, verbose=0)

    last_seq = X_data[-3:].reshape((1, 3, 1))
    pred = model.predict(last_seq, verbose=0)
    predicted = int(pred[0][0] * 9999)
    predicted = max(0, min(predicted, 9999))

    variations = []
    for _ in range(3):
        var = predicted + random.randint(-200, 200)
        var = max(0, min(var, 9999))
        variations.append(f"{var:04d}")

    return f"{predicted:04d}", variations
