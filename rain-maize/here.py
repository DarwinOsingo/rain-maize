"""
Kenya Road Construction — Linear Regression FROM SCRATCH
Target : cost_per_km  (total_cost_KES_M / road_length_km)
Method : Normal Equation  →  θ = (XᵀX)⁻¹ Xᵀy

What you'll learn in each section:
  1. Deriving a new target variable
  2. One-hot encoding categoricals (manually)
  3. Feature normalization (z-score)
  4. The Normal Equation — pure linear algebra
  5. Metrics — R², MAE, RMSE
  6. Plots — residuals, predicted vs actual, feature importance
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ── 1. LOAD DATA ──────────────────────────────────────────────────────────────
df = pd.read_csv("road_data.csv")   # <-- save your CSV as road_data.csv

# ── 2. DERIVE TARGET ──────────────────────────────────────────────────────────
# Instead of predicting raw total cost we predict COST PER KM.
# This removes the "longer road = more expensive" effect and tells us
# what actually drives the RATE of spending.
df["cost_per_km"] = df["total_cost_KES_M"] / df["road_length_km"]

# ── 3. SELECT FEATURES ────────────────────────────────────────────────────────
numeric_cols = [
    "road_length_km",
    "road_width_m",
    "num_workers",
    "dist_supplier_km",
    "num_bridges",
    "num_culverts",
]

categorical_cols = [
    "location_type",      # Urban / Rural / Peri-Urban
    "terrain",            # Flat / Hilly / Rolling / Mountainous
    "climate",            # Arid / Semi-Arid / Humid / Highland
    "soil_type",          # Clay / Loam / Sandy / Rocky
    "construction_season" # Dry / Rainy
]

# ── 4. ONE-HOT ENCODE CATEGORICALS (manually) ─────────────────────────────────
# One-hot encoding turns a category like "Terrain" into binary columns:
#   Flat=1,0,0,0  |  Hilly=0,1,0,0  |  Rolling=0,0,1,0  |  Mountainous=0,0,0,1
# We drop the FIRST category per group to avoid the dummy variable trap
# (multicollinearity — two columns that always sum to 1 confuse the math).

ohe_frames = []
for col in categorical_cols:
    dummies = pd.get_dummies(df[col], prefix=col, drop_first=True).astype(float)
    ohe_frames.append(dummies)

X_cat = pd.concat(ohe_frames, axis=1)
X_num = df[numeric_cols].astype(float)

# Combine into one feature matrix
X_raw = pd.concat([X_num, X_cat], axis=1)
feature_names = list(X_raw.columns)

# ── 5. TRAIN / TEST SPLIT (80 / 20) ──────────────────────────────────────────
# We do this BEFORE normalizing so test data never influences the scaler.
np.random.seed(42)
n = len(X_raw)
indices = np.random.permutation(n)
split = int(0.8 * n)
train_idx, test_idx = indices[:split], indices[split:]

X_train_raw = X_raw.values[train_idx]
X_test_raw  = X_raw.values[test_idx]
y_train      = df["cost_per_km"].values[train_idx]
y_test       = df["cost_per_km"].values[test_idx]

# ── 6. NORMALIZE FEATURES (z-score) ──────────────────────────────────────────
# z = (x - mean) / std
# This puts every feature on the same scale so large numbers
# (e.g. dist_supplier_km up to 600) don't dominate small ones (e.g. num_bridges).
# IMPORTANT: compute mean/std on TRAIN only, apply to both.

mean = X_train_raw.mean(axis=0)
std  = X_train_raw.std(axis=0)
std[std == 0] = 1   # avoid divide-by-zero for constant columns (rare in OHE)

X_train = (X_train_raw - mean) / std
X_test  = (X_test_raw  - mean) / std

# ── 7. ADD BIAS COLUMN ────────────────────────────────────────────────────────
# The bias (intercept) is a column of 1s prepended to X.
# It lets the model fit a line that doesn't pass through the origin.
def add_bias(X):
    return np.hstack([np.ones((X.shape[0], 1)), X])

X_train_b = add_bias(X_train)
X_test_b  = add_bias(X_test)

# ── 8. NORMAL EQUATION ────────────────────────────────────────────────────────
# The closed-form solution to linear regression:
#
#   θ = (XᵀX)⁻¹ Xᵀy
#
# This finds the EXACT θ that minimises Mean Squared Error in one shot.
# No learning rate, no iterations — pure linear algebra.
#
# Why it works:
#   MSE loss is a bowl (convex). Setting its derivative to zero and solving
#   for θ gives the formula above.

XtX = X_train_b.T @ X_train_b          # (p+1) x (p+1)  — covariance-ish matrix
Xty = X_train_b.T @ y_train            # (p+1) x 1
theta = np.linalg.inv(XtX) @ Xty       # (p+1) x 1  — our learned weights!

print("✅ Normal Equation solved.")
print(f"   Bias (intercept): {theta[0]:.4f}")

# ── 9. PREDICTIONS ────────────────────────────────────────────────────────────
y_train_pred = X_train_b @ theta
y_test_pred  = X_test_b  @ theta

# ── 10. METRICS ───────────────────────────────────────────────────────────────
def r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)        # residual sum of squares
    ss_tot = np.sum((y_true - y_true.mean()) ** 2) # total sum of squares
    return 1 - ss_res / ss_tot

def mae(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))

def rmse(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred) ** 2))

print("\n── MODEL PERFORMANCE ──────────────────────────────")
print(f"  Train R²   : {r2(y_train, y_train_pred):.4f}  (1.0 = perfect)")
print(f"  Test  R²   : {r2(y_test,  y_test_pred):.4f}")
print(f"  Test  MAE  : {mae(y_test, y_test_pred):.2f}  KES M per km")
print(f"  Test  RMSE : {rmse(y_test, y_test_pred):.2f}  KES M per km")

# ── 11. FEATURE IMPORTANCE ────────────────────────────────────────────────────
# Because we z-scored all features, the MAGNITUDE of θ tells us how much
# each feature moves the prediction per standard-deviation change.
# Larger |θ| = stronger influence on cost-per-km.

weights = theta[1:]   # drop the bias
importance = pd.Series(np.abs(weights), index=feature_names).sort_values(ascending=False)

print("\n── TOP 10 FEATURES BY |WEIGHT| ────────────────────")
print(importance.head(10).to_string())

# ── 12. PLOTS ────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 12))
fig.suptitle("Kenya Road Cost-per-km — Linear Regression (Normal Equation)",
             fontsize=14, fontweight="bold")
gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.4, wspace=0.35)

# — Plot A: Predicted vs Actual ─────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
all_vals = np.concatenate([y_test, y_test_pred])
lims = [all_vals.min() * 0.9, all_vals.max() * 1.1]
ax1.scatter(y_test, y_test_pred, alpha=0.7, edgecolors="k", linewidths=0.4, color="#2563eb")
ax1.plot(lims, lims, "r--", linewidth=1.5, label="Perfect fit")
ax1.set_xlim(lims); ax1.set_ylim(lims)
ax1.set_xlabel("Actual cost per km (KES M)"); ax1.set_ylabel("Predicted cost per km (KES M)")
ax1.set_title(f"Predicted vs Actual  (Test R²={r2(y_test, y_test_pred):.3f})")
ax1.legend()

# — Plot B: Residuals ───────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
residuals = y_test - y_test_pred
ax2.scatter(y_test_pred, residuals, alpha=0.7, edgecolors="k", linewidths=0.4, color="#16a34a")
ax2.axhline(0, color="red", linestyle="--", linewidth=1.5)
ax2.set_xlabel("Predicted cost per km (KES M)"); ax2.set_ylabel("Residual (Actual − Predicted)")
ax2.set_title("Residual Plot\n(random scatter = good; patterns = model missing something)")

# — Plot C: Residual Distribution ──────────────────────────────────
ax3 = fig.add_subplot(gs[1, 0])
ax3.hist(residuals, bins=12, color="#7c3aed", edgecolor="white", alpha=0.85)
ax3.axvline(0, color="red", linestyle="--", linewidth=1.5)
ax3.set_xlabel("Residual (KES M per km)"); ax3.set_ylabel("Count")
ax3.set_title("Distribution of Residuals\n(bell-shaped around 0 = good)")

# — Plot D: Feature Importance (top 12) ─────────────────────────────
ax4 = fig.add_subplot(gs[1, 1])
top = importance.head(12)
colors = ["#dc2626" if w > 0 else "#2563eb"
          for w in weights[importance.head(12).index.map(lambda n: list(feature_names).index(n))]]
ax4.barh(top.index[::-1], top.values[::-1], color=colors[::-1], edgecolor="white")
ax4.set_xlabel("|θ| — weight magnitude (z-scored features)")
ax4.set_title("Feature Importance\n(larger bar = stronger effect on cost-per-km)")

plt.savefig("road_regression_plots.png", dpi=150, bbox_inches="tight")
print("\n✅ Plots saved to road_regression_plots.png")
plt.show()
PYEOF
echo 