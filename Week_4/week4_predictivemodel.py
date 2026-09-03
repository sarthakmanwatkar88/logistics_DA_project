import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

import matplotlib.pyplot as plt


# ============================================================
# 1. LOAD DATASET
# ============================================================

data = pd.read_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\logistics_DA_project\Delivery_Logistics.csv"
)

print("Dataset loaded successfully!")
print("Shape:", data.shape)

print("\nColumns:")
print(data.columns.tolist())


# ============================================================
# 2. CLEAN TIME COLUMNS
# ============================================================

# The original CSV stores these columns as timestamp-like values.
# We extract the nanosecond value so they can be used as numeric hours.

data["delivery_time_hours"] = (
    pd.to_datetime(data["delivery_time_hours"]).dt.nanosecond
)

data["expected_time_hours"] = (
    pd.to_datetime(data["expected_time_hours"]).dt.nanosecond
)

print("\nTime columns converted successfully.")

print(
    data[
        ["delivery_time_hours", "expected_time_hours"]
    ].head()
)


# ============================================================
# 3. DEFINE TARGET AND FEATURES
# ============================================================

target = "delivery_time_hours"

features = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition",
    "distance_km",
    "package_weight_kg",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost"
]

X = data[features]
y = data[target]

print("\nTarget variable:", target)
print("Number of input features:", len(features))
print("X shape:", X.shape)
print("y shape:", y.shape)


# ============================================================
# 4. SPLIT DATA
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ============================================================
# 5. IDENTIFY FEATURE TYPES
# ============================================================

categorical_features = [
    "delivery_partner",
    "package_type",
    "vehicle_type",
    "delivery_mode",
    "region",
    "weather_condition"
]

numerical_features = [
    "distance_km",
    "package_weight_kg",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost"
]


# ============================================================
# 6. DATA PREPROCESSING
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)

print("\nPreprocessing setup completed.")
print("Categorical features:", len(categorical_features))
print("Numerical features:", len(numerical_features))


# ============================================================
# 7. LINEAR REGRESSION MODEL
# ============================================================

linear_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ]
)

linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_test)

print("\nLinear Regression model trained successfully!")


# ============================================================
# 8. EVALUATE LINEAR REGRESSION
# ============================================================

linear_mae = mean_absolute_error(
    y_test,
    linear_predictions
)

linear_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        linear_predictions
    )
)

linear_r2 = r2_score(
    y_test,
    linear_predictions
)

print("\n--- Linear Regression Results ---")
print("MAE:", round(linear_mae, 4))
print("RMSE:", round(linear_rmse, 4))
print("R² Score:", round(linear_r2, 4))


# ============================================================
# 9. RANDOM FOREST MODEL
# ============================================================

random_forest_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

random_forest_model.fit(X_train, y_train)

random_forest_predictions = random_forest_model.predict(X_test)

print("\nRandom Forest model trained successfully!")


# ============================================================
# 10. EVALUATE RANDOM FOREST
# ============================================================

rf_mae = mean_absolute_error(
    y_test,
    random_forest_predictions
)

rf_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        random_forest_predictions
    )
)

rf_r2 = r2_score(
    y_test,
    random_forest_predictions
)

print("\n--- Random Forest Results ---")
print("MAE:", round(rf_mae, 4))
print("RMSE:", round(rf_rmse, 4))
print("R² Score:", round(rf_r2, 4))


# ============================================================
# 11. MODEL COMPARISON
# ============================================================

results = pd.DataFrame({
    "Model": [
        "Linear Regression",
        "Random Forest"
    ],
    "MAE": [
        linear_mae,
        rf_mae
    ],
    "RMSE": [
        linear_rmse,
        rf_rmse
    ],
    "R2": [
        linear_r2,
        rf_r2
    ]
})

print("\n================ MODEL COMPARISON ================")
print(results.to_string(index=False))


# ============================================================
# 12. CROSS-VALIDATION
# ============================================================

print("\nRunning cross-validation...")

linear_cv = cross_val_score(
    linear_model,
    X_train,
    y_train,
    cv=5,
    scoring="r2"
)

rf_cv = cross_val_score(
    random_forest_model,
    X_train,
    y_train,
    cv=5,
    scoring="r2"
)

print("\n--- 5-Fold Cross-Validation ---")

print(
    "Linear Regression Mean R²:",
    round(linear_cv.mean(), 4)
)

print(
    "Random Forest Mean R²:",
    round(rf_cv.mean(), 4)
)


# ============================================================
# 13. SELECT BEST MODEL
# ============================================================

if rf_r2 > linear_r2:
    best_model = "Random Forest"
else:
    best_model = "Linear Regression"

print("\nBest model based on R² score:", best_model)


# ============================================================
# 14. SAVE MODEL RESULTS
# ============================================================

results.to_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\logistics_DA_project\Week_4\model_results.csv",
    index=False
)

print("\nModel results saved successfully!")


# ============================================================
# 15. ACTUAL VS PREDICTED DELIVERY TIME
# ============================================================

print("\nCreating actual vs predicted chart...")

plt.figure(figsize=(8, 6))

plt.scatter(
    y_test,
    linear_predictions,
    alpha=0.5,
    label="Linear Regression"
)

plt.scatter(
    y_test,
    random_forest_predictions,
    alpha=0.5,
    label="Random Forest"
)

plt.xlabel("Actual Delivery Time (hours)")
plt.ylabel("Predicted Delivery Time (hours)")
plt.title("Actual vs Predicted Delivery Time")
plt.legend()
plt.grid(True)

plt.tight_layout()

plt.savefig(
    r"C:\Users\Lenovo\OneDrive\Desktop\logistics_DA_project\Week_4\actual_vs_predicted.png"
)

plt.close()

print("Actual vs predicted chart saved successfully!")


# ============================================================
# 16. MODEL COMPARISON - R² SCORE
# ============================================================

print("\nCreating model comparison chart...")

plt.figure(figsize=(7, 5))

models = results["Model"]
r2_scores = results["R2"]

plt.bar(
    models,
    r2_scores
)

plt.xlabel("Model")
plt.ylabel("R² Score")
plt.title("Model Comparison Based on R² Score")
plt.ylim(0, 1)
plt.grid(axis="y")

plt.tight_layout()

plt.savefig(
    r"C:\Users\Lenovo\OneDrive\Desktop\logistics_DA_project\Week_4\model_comparison_r2.png"
)

plt.close()

print("Model comparison chart saved successfully!")


# ============================================================
# 17. RANDOM FOREST FEATURE IMPORTANCE
# ============================================================

print("\nCreating feature importance chart...")

# The Random Forest pipeline uses the step name "model"
rf_preprocessor = random_forest_model.named_steps["preprocessor"]
rf_model = random_forest_model.named_steps["model"]

feature_names = rf_preprocessor.get_feature_names_out()

feature_importance = rf_model.feature_importances_

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": feature_importance
})

importance_df = importance_df.sort_values(
    by="Importance",
    ascending=False
).head(10)

plt.figure(figsize=(9, 6))

plt.barh(
    importance_df["Feature"],
    importance_df["Importance"]
)

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Top 10 Random Forest Feature Importances")

plt.gca().invert_yaxis()

plt.grid(axis="x")

plt.tight_layout()

plt.savefig(
    r"C:\Users\Lenovo\OneDrive\Desktop\logistics_DA_project\Week_4\feature_importance.png"
)

plt.close()

print("Feature importance chart saved successfully!")
print("\n--- TOP 10 IMPORTANT FEATURES ---")
print(importance_df.to_string(index=False))


# ============================================================
# 18. FINAL COMPLETION MESSAGE
# ============================================================

print("\n================================================")
print("Week 4 predictive analysis completed successfully!")
print("All model results and visualizations were saved.")
print("================================================")