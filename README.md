# Real-Time Customer CDP & LTV Prediction Dashboard

A customer data platform and analytics project that combines customer behavior analysis, rule-based Customer Lifetime Value (LTV) estimation, XGBoost regression, customer segmentation, campaign recommendations, MySQL, and Power BI.

The project demonstrates how customer-level behavioral data can be transformed into actionable customer insights and visualized through an interactive dashboard.

---

## Project Overview

Customer Data Platforms (CDPs) help organizations consolidate customer information and use it for analytics, segmentation, personalization, and marketing decisions.

This project focuses on one important use case:

> Predict customer lifetime value and use the prediction to identify customer segments and recommend appropriate marketing campaigns.

The pipeline generates customer-level behavioral data, calculates a business-rule LTV baseline, trains an XGBoost regression model, compares the machine-learning model with the rule-based baseline, selects the better-performing approach, segments customers, recommends campaigns, stores the results in MySQL, and visualizes the results using Power BI.

---

## Project Architecture

```text
Customer Data
      |
      v
Feature Engineering
      |
      v
Rule-Based LTV Baseline
      |
      v
XGBoost Regression Model
      |
      v
Model Evaluation
      |
      v
Select Better Model
      |
      v
Predicted 12-Month LTV
      |
      v
Customer Segmentation
      |
      v
Campaign Recommendation
      |
      v
MySQL
      |
      v
Power BI Dashboard
```

---

## Key Features

- Synthetic customer data generation for demonstration
- Customer behavior feature engineering
- Rule-based LTV calculation
- XGBoost-based LTV regression
- Comparison between rule-based and machine-learning predictions
- MAE, RMSE, and R² evaluation
- Automatic model selection based on MAE
- Customer segmentation
- Marketing campaign recommendations
- MySQL data storage
- Power BI dashboard integration
- Environment-based database configuration
- New synthetic customer data generated on each execution

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and machine-learning pipeline |
| NumPy | Numerical operations and synthetic data generation |
| Pandas | Data manipulation |
| Scikit-learn | Train/test split and model evaluation |
| XGBoost | LTV regression model |
| SQLAlchemy | Database connectivity |
| PyMySQL | MySQL connection |
| python-dotenv | Environment variable management |
| MySQL | Customer data storage |
| Power BI | Dashboard and business visualization |

---

## LTV Prediction Approach

The project uses a hybrid approach consisting of:

1. A rule-based LTV baseline
2. An XGBoost regression model

### 1. Rule-Based LTV

The initial LTV estimate is calculated using customer behavioral factors such as:

- Days since last order
- Total number of orders
- Average order value
- Customer tenure

Business rules are applied through recency, frequency, and tenure factors.

The resulting value is used as a business baseline and is also provided to XGBoost as an engineered feature.

The rule-based value is **not treated as ground truth**.

---

### 2. XGBoost Regression

XGBoost is used as the machine-learning model because the problem is a regression problem involving numerical customer behavior features and potentially non-linear relationships.

The model receives:

- Days since last order
- Total orders
- Average order value
- Tenure
- Rule-based LTV

The model predicts customer LTV.

---

## Why XGBoost?

XGBoost was selected because it is well suited to structured/tabular data and can model non-linear relationships between customer behavior and LTV.

It also provides strong predictive performance while allowing the project to remain relatively lightweight compared with more complex deep-learning approaches.

Other models such as Linear Regression, Random Forest, and other gradient-boosting methods could also be evaluated in a production or extended version.

---

## Model Evaluation

Because LTV prediction is a regression problem, classification accuracy is not the primary evaluation metric.

The project evaluates the models using:

### Mean Absolute Error (MAE)

MAE represents the average absolute difference between predicted and actual LTV.

Lower MAE is better.

### Root Mean Squared Error (RMSE)

RMSE gives more weight to larger prediction errors.

Lower RMSE is better.

### R² Score

R² measures how much of the variation in the target variable is explained by the model.

Higher R² is generally better.

---

## Model Selection

The XGBoost model and rule-based baseline are evaluated on the same test dataset.

The model with the lower MAE is selected as the final LTV prediction method.

The selected prediction is stored in:

```text
predicted_12m_ltv
```

This column is intentionally preserved for compatibility with the Power BI dashboard.

---

## Customer Segmentation

Customers are segmented using their recency and predicted LTV.

The current segments include:

| Condition | Segment | Recommended Campaign |
|---|---|---|
| High LTV and inactive for more than 90 days | At-Risk | Win-Back Offer |
| Inactive for more than 90 days | Lost | Re-Engagement Push |
| High predicted LTV | VIP | VIP Exclusive Discount |
| Other active customers | Loyal | Loyalty Rewards |

These segments demonstrate how predictive analytics can be connected to marketing actions.

---

## MySQL Integration

The final customer-level results are written to the MySQL database:

```text
enterprise_cdp
```

The output table is:

```text
real_time_customer_cdp
```

The table contains customer information, LTV predictions, customer segments, and campaign recommendations.

Important output columns include:

```text
customer_id
days_since_last_order
total_orders
avg_order_value
tenure_days
rule_based_ltv
xgboost_ltv
predicted_12m_ltv
selected_model
customer_segment
recommended_campaign
```

The application also records a run timestamp so each execution can be identified.

---

## Power BI Dashboard

Power BI is used to visualize the customer-level results stored in MySQL.

The dashboard provides a business-facing view of:

- Total customers
- Predicted customer LTV
- Customer segments
- High-value customers
- At-risk customers
- Customer behavior
- Recommended campaigns
- LTV distribution and customer-level insights

After the Python pipeline updates MySQL, the Power BI dataset should be refreshed to retrieve the latest results.

---

## Project Setup

### 1. Clone the Repository

```bash
git clone https://github.com/gayansb45-coder/realtime-customer-cdp-dashboard.git
```

Move into the project directory:

```bash
cd realtime-customer-cdp-dashboard
```

---

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

---

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## MySQL Setup

Create the required database in MySQL:

```sql
CREATE DATABASE enterprise_cdp;
```

Make sure MySQL is running on your machine.

The application expects:

```text
Host: localhost
Database: enterprise_cdp
User: root
```

---

## Environment Configuration

Database credentials should not be stored directly in the Python source code.

Create a file named:

```text
.env
```

in the project root.

Use:

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_HOST=localhost
MYSQL_DATABASE=enterprise_cdp
```

Replace:

```text
your_mysql_password
```

with your actual MySQL password.

### Security

The `.env` file contains sensitive credentials and must never be committed to GitHub.

A safe template is provided as:

```text
.env.example
```

---

## Running the Project

Activate the virtual environment and run:

```powershell
python app.py
```

The application will:

1. Generate a new synthetic customer dataset.
2. Calculate rule-based LTV.
3. Generate a synthetic target LTV for demonstration.
4. Split the data into training and testing sets.
5. Train the XGBoost regression model.
6. Generate predictions.
7. Evaluate XGBoost.
8. Evaluate the rule-based baseline.
9. Select the model with lower MAE.
10. Generate final LTV predictions.
11. Segment customers.
12. Recommend marketing campaigns.
13. Write the final results to MySQL.

Example completion output:

```text
======================================
PIPELINE COMPLETED
======================================
Successfully updated 'enterprise_cdp.real_time_customer_cdp'
Final model used: XGBoost
Total customers generated: 1000
Total predicted LTV: ...
Run timestamp: ...
```

---

## Synthetic Data Disclaimer

This project currently uses synthetically generated customer data for demonstration and portfolio purposes.

The `actual_ltv` target used during model training is also synthetically generated.

Therefore, the reported model metrics should **not** be interpreted as production performance.

In a real-world implementation, the model target should be constructed from historical customer behavior and observed future revenue/LTV over a defined prediction window.

---

## Production Improvements

For a production implementation, the following improvements would be appropriate:

- Replace synthetic data with real transaction and customer-event data.
- Use a properly defined future LTV prediction window.
- Use historical observed revenue as the prediction target.
- Use time-based train/test validation instead of a random split when appropriate.
- Add automated model retraining.
- Track model versions and performance over time.
- Add data-quality validation.
- Add monitoring for prediction drift and data drift.
- Use a secure secrets-management solution instead of local `.env` credentials.
- Connect the CDP to real-time customer event streams.
- Add more customer behavioral and transactional features.
- Evaluate multiple machine-learning algorithms.
- Add explainability and feature-importance analysis.
- Automate Power BI dataset refresh.

---

## Limitations

This project is a portfolio/demo implementation rather than a production CDP.

The main limitations are:

1. Customer data is synthetic.
2. The target LTV is synthetically generated.
3. The current training/testing strategy uses a random split.
4. The database table is replaced during each execution.
5. Real-time event streaming is simulated through repeated execution.
6. Model performance on synthetic data does not represent performance on real customers.

These limitations are intentional so that the project can demonstrate the complete analytical pipeline without requiring access to confidential customer data.

---

## Business Value

The project demonstrates how predictive analytics can support customer-centric decision making.

Instead of looking only at historical purchases, the system combines customer behavior with predicted LTV to identify valuable and potentially lost customers.

For example:

- High-value inactive customers can receive win-back campaigns.
- Lost customers can receive re-engagement campaigns.
- High-LTV customers can receive VIP offers.
- Loyal customers can receive loyalty rewards.

This connects machine-learning predictions to practical marketing actions.

---

## Future Scope

The project can be extended into a production-grade Customer Data Platform by integrating:

- Real-time transaction events
- Web and mobile activity
- Customer support interactions
- Marketing engagement
- Product usage
- Streaming technologies
- Automated ML pipelines
- Customer-level recommendation systems
- Real-time campaign activation
- Model monitoring
- Cloud-based data infrastructure

---

## Author

**Gayan**

GitHub:

https://github.com/gayansb45-coder

---

## License

This project is intended for educational, portfolio, and demonstration purposes.
