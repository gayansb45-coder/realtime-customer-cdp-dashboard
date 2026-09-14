import os
from dotenv import load_dotenv

load_dotenv()

import numpy as np
import pandas as pd

from sqlalchemy import create_engine, URL
from xgboost import XGBRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# =========================================================
# 1. DATABASE CONFIGURATION
# =========================================================

DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")
DB_NAME = os.getenv("MYSQL_DATABASE", "enterprise_cdp")

if not DB_PASSWORD:
    raise ValueError(
        "MYSQL_PASSWORD is not set. "
        "Please create a .env file with your MySQL password."
    )

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

engine = create_engine(connection_url)


# =========================================================
# 2. GENERATE NEW CUSTOMER DATA
# =========================================================
#
# No np.random.seed() is used here.
#
# Therefore, every time app.py is executed,
# a new synthetic customer dataset is generated.
# =========================================================

n_customers = 1000

customer_ids = [
    f"CUST_{1000 + i}"
    for i in range(n_customers)
]

days_since_last = np.random.randint(
    1,
    180,
    size=n_customers
)

total_orders = np.random.randint(
    1,
    60,
    size=n_customers
)

avg_order_val = np.random.uniform(
    15.0,
    450.0,
    size=n_customers
)

tenure_days = np.random.randint(
    30,
    1000,
    size=n_customers
)


# =========================================================
# 3. RULE-BASED LTV CALCULATION
# =========================================================
#
# This is our business/domain baseline.
#
# It uses predefined business rules rather than
# machine learning.
#
# The result is also given to XGBoost as a feature.
# =========================================================

recency_factor = np.where(
    days_since_last <= 30,
    1.20,
    np.where(
        days_since_last <= 90,
        1.00,
        0.70
    )
)

frequency_factor = np.where(
    total_orders >= 30,
    1.20,
    np.where(
        total_orders >= 10,
        1.00,
        0.80
    )
)

tenure_factor = np.where(
    tenure_days >= 365,
    1.10,
    0.90
)

rule_based_ltv = (
    total_orders
    * avg_order_val
    * (tenure_days / 365)
    * recency_factor
    * frequency_factor
    * tenure_factor
)

rule_based_ltv = np.round(
    rule_based_ltv,
    2
)


# =========================================================
# 4. CREATE SYNTHETIC HISTORICAL / ACTUAL LTV
# =========================================================
#
# IMPORTANT:
#
# In a real production project, actual_ltv should come
# from historical customer revenue / observed future LTV.
#
# Here it is synthetically generated for demonstration.
# =========================================================

noise = np.random.normal(
    loc=0,
    scale=250,
    size=n_customers
)

actual_ltv = (
    total_orders
    * avg_order_val
    * (tenure_days / 365)
    * (1 + 0.0005 * days_since_last)
    + noise
)

actual_ltv = np.maximum(
    actual_ltv,
    0
)

actual_ltv = np.round(
    actual_ltv,
    2
)


# =========================================================
# 5. CREATE FEATURE DATASET
# =========================================================

df = pd.DataFrame({

    "customer_id": customer_ids,

    "days_since_last_order": days_since_last,

    "total_orders": total_orders,

    "avg_order_value": np.round(
        avg_order_val,
        2
    ),

    "tenure_days": tenure_days,

    # Rule-based LTV becomes an ML feature
    "rule_based_ltv": rule_based_ltv,

    # Target variable
    "actual_ltv": actual_ltv
})


# =========================================================
# 6. DEFINE X AND Y
# =========================================================

X = df[
    [
        "days_since_last_order",
        "total_orders",
        "avg_order_value",
        "tenure_days",
        "rule_based_ltv"
    ]
]

y = df["actual_ltv"]


# =========================================================
# 7. TRAIN / TEST SPLIT
# =========================================================
#
# 80% -> Training data
# 20% -> Testing data
#
# The test data is not used during training.
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# =========================================================
# 8. TRAIN XGBOOST
# =========================================================

model = XGBRegressor(
    n_estimators=300,
    max_depth=5,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="reg:squarederror",
    random_state=42
)

model.fit(
    X_train,
    y_train
)


# =========================================================
# 9. XGBOOST PREDICTION
# =========================================================

xgb_predictions = model.predict(
    X_test
)

# LTV cannot be negative
xgb_predictions = np.maximum(
    xgb_predictions,
    0
)

xgb_predictions = np.round(
    xgb_predictions,
    2
)


# =========================================================
# 10. EVALUATE XGBOOST
# =========================================================

xgb_mae = mean_absolute_error(
    y_test,
    xgb_predictions
)

xgb_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        xgb_predictions
    )
)

xgb_r2 = r2_score(
    y_test,
    xgb_predictions
)


# =========================================================
# 11. EVALUATE RULE-BASED BASELINE
# =========================================================

rule_test_predictions = df.loc[
    X_test.index,
    "rule_based_ltv"
]

rule_mae = mean_absolute_error(
    y_test,
    rule_test_predictions
)

rule_rmse = np.sqrt(
    mean_squared_error(
        y_test,
        rule_test_predictions
    )
)

rule_r2 = r2_score(
    y_test,
    rule_test_predictions
)


# =========================================================
# 12. PRINT MODEL COMPARISON
# =========================================================

print("\n======================================")
print("MODEL PERFORMANCE COMPARISON")
print("======================================")

print("\nRule-Based Baseline:")
print(f"MAE  : {rule_mae:.2f}")
print(f"RMSE : {rule_rmse:.2f}")
print(f"R²   : {rule_r2:.4f}")

print("\nXGBoost:")
print(f"MAE  : {xgb_mae:.2f}")
print(f"RMSE : {xgb_rmse:.2f}")
print(f"R²   : {xgb_r2:.4f}")


# =========================================================
# 13. CHOOSE BETTER MODEL
# =========================================================
#
# Lower MAE = better model
# =========================================================

if xgb_mae < rule_mae:

    selected_model = "XGBoost"

    final_ltv = model.predict(X)

    print("\nSelected Model: XGBoost")

else:

    selected_model = "Rule-Based"

    final_ltv = df["rule_based_ltv"].values

    print("\nSelected Model: Rule-Based")


# LTV cannot be negative
final_ltv = np.maximum(
    final_ltv,
    0
)

final_ltv = np.round(
    final_ltv,
    2
)


# =========================================================
# 14. CUSTOMER SEGMENTATION
# =========================================================

segments = []
campaigns = []

for days, ltv in zip(
    days_since_last,
    final_ltv
):

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


# =========================================================
# 15. FINAL CUSTOMER DATA
# =========================================================

final_df = pd.DataFrame({

    "customer_id": customer_ids,

    "days_since_last_order": days_since_last,

    "total_orders": total_orders,

    "avg_order_value": np.round(
        avg_order_val,
        2
    ),

    "tenure_days": tenure_days,

    "rule_based_ltv": rule_based_ltv,

    "xgboost_ltv": np.round(
        np.maximum(
            model.predict(X),
            0
        ),
        2
    ),

    # Keep this column name so Power BI continues to work
    "predicted_12m_ltv": final_ltv,

    "selected_model": selected_model,

    "customer_segment": segments,

    "recommended_campaign": campaigns
})


# =========================================================
# 16. WRITE RESULTS TO MYSQL
# =========================================================

final_df.to_sql(
    name="real_time_customer_cdp",
    con=engine,
    if_exists="replace",
    index=False
)


# =========================================================
# 17. FINAL MESSAGE
# =========================================================

print(
    "\nSuccessfully updated 'enterprise_cdp' "
    "with Rule-Based + XGBoost LTV predictions!"
)

print(
    f"Final model used: {selected_model}"
)

print(
    f"Total customers generated: {len(final_df)}"
)

print(
    f"Total predicted LTV: "
    f"{final_df['predicted_12m_ltv'].sum():,.2f}"
)