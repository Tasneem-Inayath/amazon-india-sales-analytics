
# 📊 Amazon India Sales Analytics Dashboard

## 🚀 Overview

The **Amazon India Sales Analytics Dashboard** is a business intelligence solution built in **Power BI**, designed to deliver actionable insights into Amazon India’s sales performance. It empowers stakeholders to monitor KPIs, analyze customer behavior, track product trends, and optimize operations.

Future integration with **Streamlit** will enable web-based access, making the dashboard even more interactive and accessible.

---

## 🔍 Key Features

- **Sales & Revenue Analysis**
  - Total revenue, average order value, MoM & YoY trends
  - Revenue breakdown by category, region, and product

- **Customer Insights**
  - New vs returning customers
  - Retention rate and purchase behavior
![description](https://github.com/Tasneem-Inayath/amazon-india-sales-analytics/tree/8da5b84ccab0b062c8446ce410ec31017cd7ba78/EDA/eda_results/discount_analysis)

- **Order & Fulfillment Metrics**
  - Order volume, delivery performance, returns & cancellations

- **Product Performance**
  - Top-selling products, cross-sell/upsell opportunities
  - Bundle recommendations and product associations

- **Inventory & Seasonal Planning**
  - Stock trends, promotional calendar, seasonal optimization

- **Command Center**
  - KPI grid, mini-trends (sparklines), automated alerts

- **Interactive Visuals**
  - Bar charts, line charts, scatter plots, heatmaps, tree maps
  - Drill-through and slicers for dynamic exploration

---

## 📁 Datasets

- **Customers** – ID, name, location, membership type  
- **Transactions** – Order ID, customer ID, date, product, revenue  
- **Products** – Product ID, category, price, stock  
- **EDA Outputs** – Cleaned CSVs for analysis (missing values as `pd.NA`)

---

## 🛠️ Tech Stack

- **Power BI** – Dashboard development  
- **Python (pandas, numpy)** – Data cleaning & preprocessing  
- **SQL** – Data querying & transformation  
- **Streamlit (optional)** – Web-based dashboard deployment  

---

## ⚙️ Installation & Setup

```bash
git clone <repository_url>
```

1. Open the `.pbix` file in **Power BI Desktop**  
2. Load datasets or connect to your SQL database  
3. Refresh visuals to update metrics  
4. *(Optional)* Run the Streamlit app:

```bash
streamlit run main.py
```

---

## 📌 Usage

- Navigate dashboard pages to explore metrics  
- Use slicers to filter by date, category, region, or customer type  
- Hover for insights, drill down for granular views  
- Monitor KPIs from the Command Center for quick performance snapshots  

---

## 🗂️ Project Structure

```plaintext
Amazon-India-Sales-Analytics/
│
├── .venv/                      # Python virtual environment
├── datasets/                   # Raw and cleaned data files
├── EDA/                        # Exploratory analysis scripts and visuals
│   └── eda_results/            # Thematic subfolders with CSVs and PNGs
├── eda_results_all_csvs/      # Consolidated EDA outputs
├── notebook/                   # Jupyter notebooks
├── POWERBI/                    # Power BI dashboard files
├── star_schema_tables/        # Fact and dimension tables
├── main.py                     # Streamlit app (optional)
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🌱 Future Enhancements

- Full **Streamlit deployment** for web access  
- **Predictive analytics** for sales forecasting  
- **Automated alerts** via email or dashboard triggers  
- Expansion to **multi-country** sales analysis  

---
### 📂 External Datasets

- [Amazon Master Dataset (2015–2025)]([https://drive.google.com/your-link](https://drive.google.com/file/d/17N5dL9_J5M1wVVbftz0dD4tWbBtKAl0P/view?usp=drive_link))
- [Transactions Table]([https://drive.google.com/your-link](https://drive.google.com/file/d/1Xp0d0qxsGj_wqxgrPMH2jYLpISYf4TGk/view?usp=drive_link))

## 📬 Contact

**Tasneem Firdhosh**  
📧 tasneemfirdhosh2001@gamil.com

---


