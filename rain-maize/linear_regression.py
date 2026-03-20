import pandas as pd
import numpy as np

##actual code
df = pd.read_csv('rainfallmaize.csv')
x = df['rainfall_mm'].to_numpy()
y = df['maize_yield_kg_per_ha'].to_numpy()
# we normalize the ranges of values to increase the rate of convergence for gradient descent

x_mean = x.mean()
x_std = x.std()
x_norm = (x- x_mean)/x_std
#initialize parameters
m = 0.0
b = 0.0
#training loop
learning_rate = 0.01
epochs = 1000
n = len(x_norm)

for epoch in range(epochs):
    #predictions
    y_pred = m*x_norm + b
    #loss
    loss = (1/n)*np.sum((y-y_pred)**2)
    #gradients
    dm = -(2/n)*np.sum(x_norm * (y-y_pred))
    db = -(2/n)*np.sum(y-y_pred)
    #update
    m = m -learning_rate*dm
    b = m - learning_rate *db
    if epoch % 100 == 0:
        print(f"Epoch {epoch} | loss {loss:.2f}")
    # Convert slope back to original units
m_real = m / x_std
b_real = b - m_real * x_mean

print(f"\nLearned: yield = {m_real:.4f} * rainfall + {b_real:.2f}")
print(f"True baked-in: yield ≈ 1.8 * rainfall + 300")

# Final predictions and MSE on original scale
y_final = m_real * x + b_real
mse = np.mean((y - y_final) ** 2)
rmse = np.sqrt(mse)
print(f"RMSE: {rmse:.2f} kg/ha")
    
