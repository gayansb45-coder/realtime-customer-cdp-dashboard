Real-Time Customer CDP & Churn Risk Dashboard

An end-to-end Machine Learning and Business Intelligence pipeline that predicts 12-month Customer Lifetime Value (LTV), identifies churn risks using XGBoost, and streams dynamic predictions into a live Power BI dashboard via MySQL.

Tech Stack & Tools
* **Language:** Python 3.x
* **Machine Learning & Data Processing:** `xgboost`, `scikit-learn`, `pandas`, `numpy`
* **Database:** MySQL
* **Database Connector:** SQLAlchemy, PyMySQL
* **Visualization:** Power BI Desktop
* **Version Control:** Git & GitHub

Key Features
* **Dynamic Behavior Engine:** Simulates real-time customer transactional variance across 500 active accounts.
* **Predictive LTV Modeling:** Uses feature metrics (Order Recency, Total Frequency, Average Order Value, Customer Tenure) to calculate predicted 12-month value.
* **Automated Risk Segmentation:** Categorizes customers into `VIP`, `Loyal`, `At-Risk`, and `Lost` based on custom ML business rules.
* **Prescriptive Campaign Mapping:** Recommends targeted marketing actions (*Win-Back Offers*, *VIP Exclusive Discounts*, *Re-Engagement Pushes*) per segment.
* **Live Power BI Integration:** Overwrites database records dynamically to demonstrate live visual state shifts on refresh.

Architecture Pipeline
 Raw Customer Data 
       │
       ▼
 Python Engine  ──> XGBoost LTV Prediction  ──>  Segmentation Rules 
                                                             
                                                             
  MySQL Database ──> Real-Time Refresh ──> Power BI Dashboard
