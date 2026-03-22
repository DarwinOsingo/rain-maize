# culums = rainfall_mm  maize_yield_kg_per_ha

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt


df = pd.read_csv('rainfallmaize.csv')

x = df['rainfall_mm'].to_numpy()
y = df['maize_yield_kg_per_ha'].to_numpy()

x_mean = x.mean()
x_std = x.std()
x_norm = (x-x_mean)/x_std

m = 0
b = 0
learning_rate = 0.01
epochs = 1000
n = len(x_norm)

for epoch in range(epochs):
    y_pred = m * x_norm + b
    #loss
    loss = (1/n)*np.sum((y-y_pred)**2)

    #gradients
    dm = -(2/n)*np.sum(x_norm * (y-y_pred))
    db = -(2/n)*np.sum(y-y_pred)

    m = m- learning_rate*dm
    b = b- learning_rate*db
    if epoch % 100 == 0:
        print(f" Epochs {epoch}|| loss : {loss}")
    m_real = m/x_std

    b_real  = b- m_real * x_mean
    print(f"\nLearned: yield = {m_real:.4f} * rainfall + {b_real:.2f}")
    y_final = m_real*x + b_real
    mse = np.mean((y-y_final)**2)
    rmse = np.sqrt(mse)
    print(f"RMSE: {rmse:.2f} kg/ha")




