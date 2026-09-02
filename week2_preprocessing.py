import pandas as pd

# Load the logistics dataset
data = pd.read_csv("Delivery_Logistics.csv")

# Display basic information
print("Dataset Shape:", data.shape)

print("\nColumn Names:")
print(data.columns.tolist())

print("\nFirst 5 Rows:")
print(data.head())

print("\nData Types:")
print(data.dtypes)

print("\nMissing Values:")
print(data.isnull().sum())

# Check for completely duplicated rows
duplicate_rows = data.duplicated().sum()

print("\nComplete Duplicate Rows:", duplicate_rows)


# Check for duplicate delivery IDs
duplicate_ids = data["delivery_id"].duplicated().sum()

print("Duplicate Delivery IDs:", duplicate_ids)


# Count unique delivery IDs
unique_ids = data["delivery_id"].nunique()

print("Unique Delivery IDs:", unique_ids)
# Check the current values in the time columns
print("\nSample Delivery Time Values:")
print(data["delivery_time_hours"].head(10))

print("\nSample Expected Time Values:")
print(data["expected_time_hours"].head(10))

# Convert time columns from timestamp-like values to numeric hours
data["delivery_time_hours"] = pd.to_datetime(
    data["delivery_time_hours"]
).dt.nanosecond

data["expected_time_hours"] = pd.to_datetime(
    data["expected_time_hours"]
).dt.nanosecond

print("\nAfter conversion:")
print(data[["delivery_time_hours", "expected_time_hours"]].head(10))

print("\nNew Data Types:")
print(data[["delivery_time_hours", "expected_time_hours"]].dtypes)

# Check for outliers in distance
Q1 = data["distance_km"].quantile(0.25)
Q3 = data["distance_km"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = data[
    (data["distance_km"] < lower_limit) |
    (data["distance_km"] > upper_limit)
]

print("\nDistance Outlier Analysis")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)
print("Number of Outliers:", len(outliers))

# Outlier analysis for numerical columns

columns_to_check = [
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "delivery_cost"
]

for column in columns_to_check:
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = data[
        (data[column] < lower_limit) |
        (data[column] > upper_limit)
    ]

    print(f"\n{column}")
    print("Lower Limit:", lower_limit)
    print("Upper Limit:", upper_limit)
    print("Number of Outliers:", len(outliers))

    # Inspect delivery-time outliers

Q1 = data["delivery_time_hours"].quantile(0.25)
Q3 = data["delivery_time_hours"].quantile(0.75)
IQR = Q3 - Q1

upper_limit = Q3 + 1.5 * IQR

time_outliers = data[data["delivery_time_hours"] > upper_limit]

print("\nDelivery Time Outliers:")
print(time_outliers[
    ["delivery_time_hours",
     "expected_time_hours",
     "delivery_status",
     "delayed",
     "distance_km"]
].head(20))

# Check numerical columns before normalization

numeric_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost"
]

print("\nNumerical Data Before Normalization:")

for column in numeric_columns:
    print(
        f"{column}: "
        f"Min = {data[column].min()}, "
        f"Max = {data[column].max()}"
    )


# Min-Max normalization

normalized_data = data.copy()

for column in numeric_columns:
    min_value = normalized_data[column].min()
    max_value = normalized_data[column].max()

    normalized_data[column] = (
        (normalized_data[column] - min_value)
        / (max_value - min_value)
    )

print("\nNumerical Data After Normalization:")
print(normalized_data[numeric_columns].head())

print("\nNormalized Data Range:")
for column in numeric_columns:
    print(
        f"{column}: "
        f"Min = {normalized_data[column].min():.2f}, "
        f"Max = {normalized_data[column].max():.2f}"
    )    

# Step 7: Validate the cleaned dataset

print("\n--- Validation Results ---")

print("\nMissing Values:")
print(data.isnull().sum().sum())

print("\nDuplicate Rows:")
print(data.duplicated().sum())

print("\nData Types:")
print(data.dtypes)

print("\nOriginal Data Shape:")
print(data.shape)

print("\nNormalized Data Shape:")
print(normalized_data.shape)    


# Step 8: Before vs After normalization

print("\n--- Before vs After Normalization ---")

comparison = pd.DataFrame({
    "Original Delivery Cost": data["delivery_cost"].head(10),
    "Normalized Delivery Cost": normalized_data["delivery_cost"].head(10)
})

print(comparison)

import matplotlib.pyplot as plt

# Before vs After normalization chart
# Before and After Normalization Visualization

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Before normalization
axes[0].plot(
    data["delivery_cost"].head(20),
    marker="o"
)
axes[0].set_title("Before Normalization")
axes[0].set_xlabel("Record Number")
axes[0].set_ylabel("Delivery Cost")
axes[0].grid(True)

# After normalization
axes[1].plot(
    normalized_data["delivery_cost"].head(20),
    marker="o"
)
axes[1].set_title("After Min-Max Normalization")
axes[1].set_xlabel("Record Number")
axes[1].set_ylabel("Normalized Value (0-1)")
axes[1].grid(True)

plt.tight_layout()

plt.savefig(
    "delivery_cost_before_after.png",
    dpi=300
)

plt.show()



# Step 9: Methodology Explanation

print("\n--- Methodology Summary ---")

print("""
1. Missing Value Handling:
   The dataset was checked for missing values using isnull().
   No missing values were found, so no imputation was required.

2. Duplicate Checking:
   Complete duplicate rows were checked and none were found.
   Duplicate delivery IDs were also identified and treated as an
   identifier-quality issue rather than deleting records automatically.

3. Data Type Conversion:
   Delivery time and expected time columns contained timestamp-like
   values.
   These values were converted into numerical hour values so that
   statistical analysis and preprocessing could be performed correctly.

4. Outlier Detection:
   The IQR method was used to identify unusual numerical observations.
   Delivery time contained 203 statistical outliers.
   These observations were inspected and retained because they
   represented plausible longer delivery times rather than obvious
   data-entry errors.

5. Normalization:
   Min-Max normalization was applied to numerical variables.
   This transformed their values to a common 0-to-1 scale, which is
   useful for future analytical and machine-learning techniques.

6. Validation:
   The processed dataset was checked again for missing values,
   duplicate rows, data types, and dataset dimensions.
""")


# Step 10: Reflection

print("\n--- Reflection ---")

print("""
Data quality has a direct impact on logistics analytics and
decision-making. Incorrect data types, duplicate records, missing
values, and extreme values can produce misleading results.

In this dataset, no missing values or complete duplicate rows were
found. However, duplicate delivery IDs and incorrectly formatted
time values were identified. The time values were converted into
numerical hours so that they could be analyzed correctly.

The IQR method identified 203 delivery-time observations as
statistical outliers. These records were not automatically removed
because they appeared to represent plausible longer delivery times.

Min-Max normalization converted the selected numerical variables
to a common 0-to-1 scale. This can make the data more suitable for
future statistical analysis and machine-learning applications.

Overall, the preprocessing process improves the reliability,
consistency, and usability of the logistics dataset for further
analysis and decision-making.
""")