# ============================================================
# WEEK 3 - ADVANCED DATA ANALYSIS AND VISUALIZATION
# LOGISTICS DATA ANALYSIS PROJECT
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the folder where this Python file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# 1. LOAD DATASET
# ============================================================

print("\n" + "=" * 60)
print("WEEK 3 - ADVANCED DATA ANALYSIS AND VISUALIZATION")
print("=" * 60)

data = pd.read_csv(
    r"C:\Users\Lenovo\OneDrive\Desktop\logistics_DA_project\Delivery_Logistics.csv"
)

print("\nDataset loaded successfully.")


# ============================================================
# 2. BASIC DATASET INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("1. DATASET OVERVIEW")
print("=" * 60)

print("Number of rows:", data.shape[0])
print("Number of columns:", data.shape[1])

print("\nColumn names:")
print(data.columns.tolist())

print("\nData types:")
print(data.dtypes)

print("\nMissing values:")
print(data.isnull().sum())

print("\nComplete duplicate rows:", data.duplicated().sum())


# ============================================================
# 3. CLEAN DELIVERY TIME COLUMNS
# ============================================================

print("\n" + "=" * 60)
print("2. DATA TYPE CLEANING")
print("=" * 60)

data["delivery_time_hours"] = pd.to_datetime(
    data["delivery_time_hours"]
).dt.nanosecond

data["expected_time_hours"] = pd.to_datetime(
    data["expected_time_hours"]
).dt.nanosecond

data["delivery_time_hours"] = data[
    "delivery_time_hours"
].astype("int32")

data["expected_time_hours"] = data[
    "expected_time_hours"
].astype("int32")

print("Delivery time type:",
      data["delivery_time_hours"].dtype)

print("Expected time type:",
      data["expected_time_hours"].dtype)


# ============================================================
# 4. CREATE NUMERICAL DELAY VARIABLE
# ============================================================

data["delayed_numeric"] = data["delayed"].map({
    "yes": 1,
    "no": 0
})

print("\nDelay variable created.")


# ============================================================
# 5. CENTRAL TENDENCY
# ============================================================

print("\n" + "=" * 60)
print("3. CENTRAL TENDENCY")
print("=" * 60)

numeric_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost"
]

for column in numeric_columns:

    print("\n----------------------------------------")
    print(column)
    print("----------------------------------------")

    print("Mean:",
          round(data[column].mean(), 2))

    print("Median:",
          round(data[column].median(), 2))

    mode_value = data[column].mode()

    if len(mode_value) > 0:
        print("Mode:", mode_value.iloc[0])

    print("Minimum:",
          data[column].min())

    print("Maximum:",
          data[column].max())

    print("Standard deviation:",
          round(data[column].std(), 2))


# ============================================================
# 6. DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("4. DESCRIPTIVE STATISTICS")
print("=" * 60)

print(data[numeric_columns].describe())


# ============================================================
# 7. CREATE VISUALIZATION FOLDER
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

visualization_folder = os.path.join(
    BASE_DIR,
    "visualizations"
)

os.makedirs(
    visualization_folder,
    exist_ok=True
)

print("\nVisualization folder created.")


# ============================================================
# 8. DELIVERY TIME DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 6))

plt.hist(
    data["delivery_time_hours"],
    bins=20,
    edgecolor="black"
)

plt.title("Distribution of Delivery Time")
plt.xlabel("Delivery Time (Hours)")
plt.ylabel("Number of Deliveries")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delivery_time_distribution.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 9. DELIVERY COST DISTRIBUTION
# ============================================================

plt.figure(figsize=(9, 6))

plt.hist(
    data["delivery_cost"],
    bins=25,
    edgecolor="black"
)

plt.title("Distribution of Delivery Cost")
plt.xlabel("Delivery Cost")
plt.ylabel("Number of Deliveries")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delivery_cost_distribution.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 10. DELIVERY STATUS
# ============================================================

status_counts = data[
    "delivery_status"
].value_counts()

plt.figure(figsize=(8, 6))

plt.bar(
    status_counts.index,
    status_counts.values
)

plt.title("Delivery Status Distribution")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Deliveries")
plt.xticks(rotation=0)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delivery_status_distribution.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 11. DELIVERY PARTNER ANALYSIS
# ============================================================

partner_analysis = data.groupby(
    "delivery_partner"
).agg(
    total_deliveries=("delivery_id", "count"),
    average_delivery_time=("delivery_time_hours", "mean"),
    average_delivery_cost=("delivery_cost", "mean"),
    delay_rate=("delayed_numeric", "mean"),
    average_rating=("delivery_rating", "mean")
).reset_index()

partner_analysis["delay_rate_percent"] = (
    partner_analysis["delay_rate"] * 100
)

partner_analysis = partner_analysis.sort_values(
    "delay_rate_percent",
    ascending=False
)

print("\n" + "=" * 60)
print("5. DELIVERY PARTNER ANALYSIS")
print("=" * 60)

print(
    partner_analysis[
        [
            "delivery_partner",
            "total_deliveries",
            "average_delivery_time",
            "average_delivery_cost",
            "delay_rate_percent",
            "average_rating"
        ]
    ].round(2)
)


# ============================================================
# 12. PARTNER DELAY RATE
# ============================================================

plt.figure(figsize=(10, 6))

plt.bar(
    partner_analysis["delivery_partner"],
    partner_analysis["delay_rate_percent"]
)

plt.title("Delay Rate by Delivery Partner")
plt.xlabel("Delivery Partner")
plt.ylabel("Delay Rate (%)")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delay_rate_by_partner.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 13. WEATHER ANALYSIS
# ============================================================

weather_analysis = data.groupby(
    "weather_condition"
).agg(
    total_deliveries=("delivery_id", "count"),
    average_delivery_time=("delivery_time_hours", "mean"),
    delay_rate=("delayed_numeric", "mean"),
    average_cost=("delivery_cost", "mean")
).reset_index()

weather_analysis["delay_rate_percent"] = (
    weather_analysis["delay_rate"] * 100
)

weather_analysis = weather_analysis.sort_values(
    "delay_rate_percent",
    ascending=False
)

print("\n" + "=" * 60)
print("6. WEATHER CONDITION ANALYSIS")
print("=" * 60)

print(
    weather_analysis[
        [
            "weather_condition",
            "total_deliveries",
            "average_delivery_time",
            "delay_rate_percent",
            "average_cost"
        ]
    ].round(2)
)


# ============================================================
# 14. WEATHER DELAY RATE
# ============================================================

plt.figure(figsize=(9, 6))

plt.bar(
    weather_analysis["weather_condition"],
    weather_analysis["delay_rate_percent"]
)

plt.title("Delay Rate by Weather Condition")
plt.xlabel("Weather Condition")
plt.ylabel("Delay Rate (%)")
plt.xticks(rotation=30)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delay_rate_by_weather.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 15. REGIONAL ANALYSIS
# ============================================================

region_analysis = data.groupby(
    "region"
).agg(
    total_deliveries=("delivery_id", "count"),
    average_delivery_time=("delivery_time_hours", "mean"),
    average_cost=("delivery_cost", "mean"),
    delay_rate=("delayed_numeric", "mean"),
    average_rating=("delivery_rating", "mean")
).reset_index()

region_analysis["delay_rate_percent"] = (
    region_analysis["delay_rate"] * 100
)

region_analysis = region_analysis.sort_values(
    "delay_rate_percent",
    ascending=False
)

print("\n" + "=" * 60)
print("7. REGIONAL PERFORMANCE")
print("=" * 60)

print(
    region_analysis[
        [
            "region",
            "total_deliveries",
            "average_delivery_time",
            "average_cost",
            "delay_rate_percent",
            "average_rating"
        ]
    ].round(2)
)


# ============================================================
# 16. REGIONAL DELAY RATE
# ============================================================

plt.figure(figsize=(8, 6))

plt.bar(
    region_analysis["region"],
    region_analysis["delay_rate_percent"]
)

plt.title("Delay Rate by Region")
plt.xlabel("Region")
plt.ylabel("Delay Rate (%)")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delay_rate_by_region.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 17. DISTANCE VS DELIVERY TIME
# ============================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    data["distance_km"],
    data["delivery_time_hours"],
    alpha=0.35
)

plt.title("Distance vs Delivery Time")
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Time (Hours)")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "distance_vs_delivery_time.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 18. DISTANCE VS DELIVERY COST
# ============================================================

plt.figure(figsize=(9, 6))

plt.scatter(
    data["distance_km"],
    data["delivery_cost"],
    alpha=0.35
)

plt.title("Distance vs Delivery Cost")
plt.xlabel("Distance (km)")
plt.ylabel("Delivery Cost")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "distance_vs_delivery_cost.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 19. CORRELATION ANALYSIS
# ============================================================

correlation_columns = [
    "distance_km",
    "package_weight_kg",
    "delivery_time_hours",
    "expected_time_hours",
    "delivery_rating",
    "delivery_cost",
    "delayed_numeric"
]

correlation_matrix = data[
    correlation_columns
].corr()

print("\n" + "=" * 60)
print("8. CORRELATION ANALYSIS")
print("=" * 60)

print(
    correlation_matrix.round(2)
)


# ============================================================
# 20. CORRELATION HEATMAP
# ============================================================

plt.figure(figsize=(10, 8))

plt.imshow(
    correlation_matrix,
    cmap="coolwarm",
    vmin=-1,
    vmax=1
)

plt.colorbar(
    label="Correlation"
)

plt.xticks(
    range(len(correlation_columns)),
    correlation_columns,
    rotation=45,
    ha="right"
)

plt.yticks(
    range(len(correlation_columns)),
    correlation_columns
)

plt.title("Correlation Matrix of Logistics Variables")

for i in range(len(correlation_columns)):
    for j in range(len(correlation_columns)):
        plt.text(
            j,
            i,
            f"{correlation_matrix.iloc[i, j]:.2f}",
            ha="center",
            va="center",
            fontsize=8
        )

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "correlation_heatmap.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 21. AVERAGE COST BY PARTNER
# ============================================================

cost_by_partner = data.groupby(
    "delivery_partner"
)["delivery_cost"].mean().sort_values(
    ascending=False
)

print("\n" + "=" * 60)
print("9. AVERAGE DELIVERY COST BY PARTNER")
print("=" * 60)

print(
    cost_by_partner.round(2)
)

plt.figure(figsize=(10, 6))

plt.bar(
    cost_by_partner.index,
    cost_by_partner.values
)

plt.title("Average Delivery Cost by Partner")
plt.xlabel("Delivery Partner")
plt.ylabel("Average Delivery Cost")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "average_cost_by_partner.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 22. DELIVERY RATING DISTRIBUTION
# ============================================================

rating_counts = data[
    "delivery_rating"
].value_counts().sort_index()

plt.figure(figsize=(8, 6))

plt.bar(
    rating_counts.index.astype(str),
    rating_counts.values
)

plt.title("Delivery Rating Distribution")
plt.xlabel("Delivery Rating")
plt.ylabel("Number of Deliveries")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(
        visualization_folder,
        "delivery_rating_distribution.png"
    ),
    dpi=300
)

plt.show()


# ============================================================
# 23. KEY PERFORMANCE INDICATORS
# ============================================================

total_deliveries = len(data)

average_delivery_time = data[
    "delivery_time_hours"
].mean()

average_expected_time = data[
    "expected_time_hours"
].mean()

average_delivery_cost = data[
    "delivery_cost"
].mean()

overall_delay_rate = (
    data["delayed_numeric"].mean() * 100
)

average_rating = data[
    "delivery_rating"
].mean()

print("\n" + "=" * 60)
print("10. KEY LOGISTICS PERFORMANCE INDICATORS")
print("=" * 60)

print("Total deliveries:", total_deliveries)

print(
    "Average delivery time:",
    round(average_delivery_time, 2),
    "hours"
)

print(
    "Average expected time:",
    round(average_expected_time, 2),
    "hours"
)

print(
    "Average delivery cost:",
    round(average_delivery_cost, 2)
)

print(
    "Overall delay rate:",
    round(overall_delay_rate, 2),
    "%"
)

print(
    "Average delivery rating:",
    round(average_rating, 2)
)


# ============================================================
# 24. KEY FINDINGS
# ============================================================

highest_partner_delay = partner_analysis.iloc[0]
highest_weather_delay = weather_analysis.iloc[0]
highest_region_delay = region_analysis.iloc[0]
highest_cost_partner = cost_by_partner.index[0]

print("\n" + "=" * 60)
print("11. KEY ANALYTICAL FINDINGS")
print("=" * 60)

print(
    "\nPartner with highest delay rate:",
    highest_partner_delay["delivery_partner"],
    "-",
    round(
        highest_partner_delay["delay_rate_percent"],
        2
    ),
    "%"
)

print(
    "Weather condition with highest delay rate:",
    highest_weather_delay["weather_condition"],
    "-",
    round(
        highest_weather_delay["delay_rate_percent"],
        2
    ),
    "%"
)

print(
    "Region with highest delay rate:",
    highest_region_delay["region"],
    "-",
    round(
        highest_region_delay["delay_rate_percent"],
        2
    ),
    "%"
)

print(
    "Partner with highest average delivery cost:",
    highest_cost_partner
)


# ============================================================
# 25. SAVE ANALYSIS TABLES
# ============================================================

partner_analysis.to_csv(
    os.path.join(
        visualization_folder,
        "partner_analysis.csv"
    ),
    index=False
)

weather_analysis.to_csv(
    os.path.join(
        visualization_folder,
        "weather_analysis.csv"
    ),
    index=False
)

region_analysis.to_csv(
    os.path.join(
        visualization_folder,
        "region_analysis.csv"
    ),
    index=False
)

correlation_matrix.to_csv(
    os.path.join(
        visualization_folder,
        "correlation_matrix.csv"
    )
)


# ============================================================
# 26. COMPLETION MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print(
    "\nAll visualization files were saved inside:"
)

print(
    os.path.abspath(visualization_folder)
)

print("\nWeek 3 analysis is complete.")