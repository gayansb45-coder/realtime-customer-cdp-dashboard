import numpy as np
import pandas as pd
from sqlalchemy import create_engine, URL

# ---------------------------------------------------------
# 1. DATABASE CONFIGURATION (Set your password here)
# ---------------------------------------------------------
DB_USER = "root"
DB_PASSWORD = "***REMOVED***"  # <-- Change this to your real MySQL password (or "" if no password)
DB_HOST = "localhost"
DB_NAME = "enterprise_cdp"

# Safely construct the connection string without formatting bugs
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

engine = create_engine(connection_url)

# ---------------------------------------------------------
# 2. GENERATE DYNAMIC CUSTOMER DATA
# ---------------------------------------------------------
n_customers = 500
customer_ids = [f"CUST_{1000 + i}" for i in range(n_customers)]

# Inject fresh random behavior variance every time script runs
days_since_last = np.random.randint(1, 180, size=n_customers)
total_orders = np.random.randint(1, 60, size=n_customers)
avg_order_val = np.random.uniform(15.0, 450.0, size=n_customers)
tenure_days = np.random.randint(30, 1000, size=n_customers)

# Calculate LTV with dynamic market multiplier
market_multiplier = np.random.uniform(0.8, 1.5)
predicted_ltv = np.round((total_orders * avg_order_val * (tenure_days / 365)) * market_multiplier, 2)

# Dynamic segmentation and marketing assignment
segments = []
campaigns = []

for days, ltv in zip(days_since_last, predicted_ltv):
    if days > 90 and ltv > 1000:
        segments.append("At-Risk")
        campaigns.append("Win-Back Offer")
    elif days > 90:
        segments.append("Lost")
        campaigns.append("Re-Engagement Push")
    elif ltv > 3000:
        segments.append("VIP")
        campaigns.append("VIP Exclusive Discount")
    else:
        segments.append("Loyal")
        campaigns.append("Loyalty Rewards")

# Build Pandas DataFrame
df = pd.DataFrame({
    'customer_id': customer_ids,
    'days_since_last_order': days_since_last,
    'total_orders': total_orders,
    'avg_order_value': np.round(avg_order_val, 2),
    'tenure_days': tenure_days,
    'predicted_12m_ltv': predicted_ltv,
    'customer_segment': segments,
    'recommended_campaign': campaigns
})

# ---------------------------------------------------------
# 3. WRITE TO MYSQL
# ---------------------------------------------------------
df.to_sql(name='real_time_customer_cdp', con=engine, if_exists='replace', index=False)
print("Successfully updated 'enterprise_cdp' database with fresh dynamic predictions!")