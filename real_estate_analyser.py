import pandas as pd

# Let's create a simulated list of Tampa properties
# In a real AI project, you'd pull this from an API or a CSV
properties = [
    {"address": "123 Clearwater Ln", "price": 380000, "sqft": 1500, "type": "Single Family"},
    {"address": "456 Tampa Bay Blvd", "price": 425000, "sqft": 1800, "type": "Single Family"},
    {"address": "789 Gulf Way", "price": 315000, "sqft": 1100, "type": "Condo"},
    {"address": "101 Palm St", "price": 410000, "sqft": 1700, "type": "Single Family"},
]

# Convert to a DataFrame (our "Table")
df = pd.DataFrame(properties)

# Logic: You want a home between $350k and $415k
budget_min = 350000
budget_max = 415000

# Filter the data
matches = df[(df['price'] >= budget_min) & (df['price'] <= budget_max)]

print(f"--- Found {len(matches)} properties in your budget range ---")
print(matches)

# Bonus: Calculate the average Price per Square Foot
df['price_per_sqft'] = df['price'] / df['sqft']
print("\n--- Average Price per SqFt for all listings ---")
print(f"${df['price_per_sqft'].mean():.2f}")