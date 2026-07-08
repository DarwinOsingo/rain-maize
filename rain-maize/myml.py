# location_type,terrain,climate,soil_type,construction_season,road_length_km,road_width_m,num_workers,dist_supplier_km,num_bridges,num_culverts,total_cost_KES_M
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('kenya_roads.csv')

# --- DERIVE TARGET ---
df['cost_per_km'] = df['total_cost_KES_M'] / df['road_length_km']

df = pd.get_dummies(df, columns=["location_type", "climate", "construction_season", "terrain", "soil_type"], drop_first=True)
df = df.drop(columns=['project_id', 'total_cost_KES_M'])

# --- FEATURES & TARGET ---
X = df.drop(columns=['cost_per_km']).values.astype(float)
y = df['cost_per_km'].values.astype(float)
feature_names = df.drop(columns=['cost_per_km']).columns.tolist()

# --- TRAIN/TEST SPLIT (80/20) ---
np.random.seed(42)
indices = np.random.permutation(len(X))
split = int(0.8 * len(X))
train_idx, test_idx = indices[:split], indices[split:]

X_train, X_test = X[train_idx], X[test_idx]
y_train, y_test = y[train_idx], y[test_idx]

# --- NORMALIZE (z-score) ---
# subtract mean, divide by std so all features are on the same scale
# we compute mean/std on train only — test data must not influence the scaler
mean = X_train.mean(axis=0)
std  = X_train.std(axis=0)
std[std == 0] = 1  # avoid divide-by-zero on constant columns

X_train = (X_train - mean) / std
X_test  = (X_test  - mean) / std

# --- ADD BIAS COLUMN (column of 1s) ---
# gives the model an intercept — lets the line not pass through the origin
X_train_b = np.hstack([np.ones((X_train.shape[0], 1)), X_train])
X_test_b  = np.hstack([np.ones((X_test.shape[0],  1)), X_test])

# --- NORMAL EQUATION: theta = (XtX)^-1 Xty ---
# closed-form solution — finds the exact best weights in one step, no iterations
theta = np.linalg.inv(X_train_b.T @ X_train_b) @ (X_train_b.T @ y_train)

# --- PREDICTIONS ---
y_train_pred = X_train_b @ theta
y_test_pred  = X_test_b  @ theta

# --- METRICS ---
def r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - y_true.mean()) ** 2)
    return 1 - ss_res / ss_tot

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

print(f"Train R²  : {r2(y_train, y_train_pred):.4f}")
print(f"Test  R²  : {r2(y_test,  y_test_pred):.4f}")
print(f"Test  MAE : {mae(y_test, y_test_pred):.2f} KES M per km")
print(f"Test  RMSE: {rmse(y_test, y_test_pred):.2f} KES M per km")

# --- FEATURE IMPORTANCE ---
# because features are z-scored, |theta| tells us how much each
# feature shifts the prediction per standard deviation
weights = theta[1:]  # skip bias
importance = pd.Series(np.abs(weights), index=feature_names).sort_values(ascending=False)
print("\nTop 10 features by weight magnitude:")
print(importance.head(10).to_string())

# --- PLOTS ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Kenya Road Cost-per-km — Linear Regression (Normal Equation)", fontweight='bold')

# predicted vs actual
axes[0,0].scatter(y_test, y_test_pred, alpha=0.7, edgecolors='k', linewidths=0.4)
lims = [min(y_test.min(), y_test_pred.min()) * 0.9, max(y_test.max(), y_test_pred.max()) * 1.1]
axes[0,0].plot(lims, lims, 'r--')
axes[0,0].set_xlabel('Actual'); axes[0,0].set_ylabel('Predicted')
axes[0,0].set_title(f'Predicted vs Actual  (R2={r2(y_test, y_test_pred):.3f})')

# residuals
residuals = y_test - y_test_pred
axes[0,1].scatter(y_test_pred, residuals, alpha=0.7, edgecolors='k', linewidths=0.4)
axes[0,1].axhline(0, color='red', linestyle='--')
axes[0,1].set_xlabel('Predicted'); axes[0,1].set_ylabel('Residual')
axes[0,1].set_title('Residual Plot')

# residual distribution
sns.histplot(residuals, bins=12, ax=axes[1,0], kde=True)
axes[1,0].axvline(0, color='red', linestyle='--')
axes[1,0].set_xlabel('Residual (KES M per km)')
axes[1,0].set_title('Residual Distribution')

# feature importance
top = importance.head(12)
axes[1,1].barh(top.index[::-1], top.values[::-1])
axes[1,1].set_xlabel('|theta| weight magnitude')
axes[1,1].set_title('Feature Importance')

plt.tight_layout()
plt.savefig('road_regression_plots.png', dpi=150, bbox_inches='tight')
plt.show()