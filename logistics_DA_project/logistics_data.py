
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("Delivery_logistics.csv")

clean_data = data.copy()

clean_data["delivery_time_hours"] = (
    pd.to_datetime(clean_data["delivery_time_hours"])
    .dt.nanosecond
)

clean_data["expected_time_hours"] = (
    pd.to_datetime(clean_data["expected_time_hours"])
    .dt.nanosecond
)

total_deliveries = len(clean_data)

delayed_deliveries = (clean_data["delayed"] == "yes").sum()

delay_rate = (delayed_deliveries / total_deliveries) * 100

print("Total deliveries:", total_deliveries)
print("Delayed deliveries:", delayed_deliveries)
print("Delay rate:", delay_rate, "%")

average_delivery_time = clean_data["delivery_time_hours"].mean()

print("Average delivery time:", average_delivery_time, "hours")

average_delivery_cost = clean_data["delivery_cost"].mean()

print("Average delivery cost:", average_delivery_cost)

failed_deliveries = (clean_data["delivery_status"] == "failed").sum()

failure_rate = (failed_deliveries / total_deliveries) * 100

print("Failed deliveries:", failed_deliveries)
print("Failure rate:", failure_rate, "%")
print(clean_data["delivery_partner"].value_counts())

partner_delivery_time = clean_data.groupby(
    "delivery_partner"
)["delivery_time_hours"].mean()

print(partner_delivery_time.sort_values())

delay_by_partner = clean_data.groupby("delivery_partner")["delayed"].apply(
    lambda x: (x == "yes").mean() * 100
)

print(delay_by_partner.sort_values(ascending=False))

print(clean_data["weather_condition"].value_counts())

delay_by_weather = clean_data.groupby("weather_condition")["delayed"].apply(
    lambda x: (x == "yes").mean() * 100
)

print(delay_by_weather.sort_values(ascending=False))

print(clean_data["region"].value_counts())



delay_by_region = clean_data.groupby("region")["delayed"].apply(
    lambda x: (x == "yes").mean() * 100
)

print(delay_by_region.sort_values(ascending=False))


plt.figure(figsize=(10, 5))

delay_by_partner.sort_values().plot(kind="barh")

plt.title("Delay Rate by Delivery Partner")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Delivery Partner")

plt.tight_layout()


plt.figure(figsize=(10, 5))

delay_by_weather.sort_values().plot(kind="barh")

plt.title("Delay Rate by Weather Condition")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Weather Condition")

plt.tight_layout()

plt.figure(figsize=(10, 5))

delay_by_region.sort_values().plot(kind="barh")

plt.title("Delay Rate by Region")
plt.xlabel("Delay Rate (%)")
plt.ylabel("Region")

plt.tight_layout()

plt.show()