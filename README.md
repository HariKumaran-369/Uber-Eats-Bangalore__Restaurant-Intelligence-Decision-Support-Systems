# Uber Eats Bangalore — Restaurant Intelligence & Decision Support System

A SQL-powered business analytics platform that analyses Uber Eats restaurant data for Bangalore, answers 12 critical business questions through SQL queries, and presents all insights as clean tabular outputs in a Streamlit web application — with no charts or visualisations, mirroring real internal analytics dashboards.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Demo

🎥 Watch the demo video: **[ https://www.linkedin.com/posts/hari-kumaran-369univers_python-streamlit-sqlite-activity-7480992982410756097-Ib2a?utm_source=share&utm_medium=member_desktop&rcm=ACoAAGN887EBYUAxkSV4oyB8GqsP28FYWJbguCo ]**

---

## Overview

This project loads Uber Eats Bangalore restaurant data from CSV, cleans and normalises it using Pandas, stores it in a SQLite relational database, and then answers 15 predefined business questions entirely through SQL queries. The results are surfaced in a three-page Streamlit application that supports dynamic filtering, a full question-and-answer panel, and order data analytics.

All filtering and aggregation logic is implemented strictly using SQL — no Python-level filtering of DataFrames.

---

## Business Use Cases

- Location Intelligence — identify premium and oversaturated areas
- Partner Onboarding Strategy — find ideal locations for new restaurants
- Pricing Optimisation — determine which price tier drives best ratings
- Cuisine Performance Analysis — surface high-performing and niche cuisines
- Platform Feature Impact — measure the ROI of online ordering and table booking
- Market Segmentation — group restaurants by price, rating, and feature adoption
- Customer Satisfaction Drivers — correlate cost, features, and ratings
- Expansion Planning — identify premium locations ready for growth

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data Cleaning | Pandas, NumPy |
| Database | SQLite (via sqlite3 — built in to Python) |
| Analytics | SQL (GROUP BY, HAVING, CASE WHEN, Window Functions) |
| Web Application | Streamlit |

---

## Project Architecture

Uber_Eats_data.csv + orders.json (Raw Data)
       │
       ▼
clean_data.py (Pandas – clean, normalise, feature engineer)
       │
       ▼
uber_eats_cleaned.csv (Cleaned Dataset)
       │
       ▼
database.py (SQLite – create tables, insert data)
       │
       ▼
uber_eats.db (SQLite database file)
       │
       ▼
queries.py (uber_eats-13, order_rows-5, SQL business questions)
       │
       ▼
app.py (Streamlit – Dashboard | Business Q&A | Order Analytics)


---

## Folder Structure

```
uber_eats_project/
│
├── data/
│   ├── orders.json
│   ├── uber_eats_cleaned.csv
│   └── Uber_Eats_data.csv
│
├── app.py
├── clean_data.py
├── database.py
├── queries.py
├── README.md
├── requirements.txt
└── uber_eats.db
```

---

## Dataset

| File | Description |
|---|---|
| `Uber_eats_data.csv` | Uber Eats Bangalore restaurant records |
| `orders.json` | Order transaction records with restaurant, date, value, payment, and discount fields |

### Key Columns — Uber_eats_data.csv

| Column | Description |
|---|---|
| `name` | Restaurant name |
| `location` | Bangalore neighbourhood |
| `cuisines` | Cuisine types served |
| `rate` | Customer rating (e.g. "4.2/5") |
| `votes` | Number of customer votes |
| `approx_cost(for two people)` | Approximate cost for two diners |
| `online_order` | Whether online ordering is available (Yes/No) |
| `book_table` | Whether table booking is available (Yes/No) |
| `rest_type` | Restaurant type (e.g. Casual Dining, Café) |
| `dish_liked` | Most liked dishes |

### Key Columns — orders.json

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `restaurant_name` | Name of the restaurant |
| `order_date` | Date of the order |
| `order_value` | Total order amount in INR |
| `discount_used` | Whether a discount was applied (Yes/No) |
| `payment_method` | Payment method used (Card, Cash, UPI, etc.) |

---

## Methodology

1. **Data Cleaning** (`clean_data.py`) — Removes duplicates, fills missing values, cleans the rate column (`"4.2/5"` → `4.2`), standardises the cost column (`"₹1,200"` → `1200`), converts Yes/No to 1/0, and engineers two new columns: `price_segment` (Low / Mid / Premium) and `rating_category` (Poor / Average / Good / Excellent).

2. **Database Layer** (`database.py`) — Creates a SQLite database (`uber_eats.db`) with a `restaurants` table and an `orders` table. Inserts the cleaned DataFrame using `pandas.DataFrame.to_sql()`.

3. **SQL Analytics** (`queries.py`) — Defines 15 business question functions. Each executes a cursor-based SQL query against the SQLite database and returns a Pandas DataFrame. Heavy use of `GROUP BY`, `HAVING`, `CASE WHEN`, `ROW_NUMBER() OVER (PARTITION BY ...)`, and sub-queries.

4. **Streamlit Application** (`app.py`) — A three-page app: Dashboard (dynamic SQL filter builder), Business Q&A (run one or all 13 questions), and Order Analytics (six SQL-driven order insights).

---

## 15 Business Questions

| # | Question | Business Value |
|---|---|---|
| Q1 | Which locations have the highest average ratings? | Premium partner onboarding areas |
| Q2 | Which locations are over-saturated? | Avoid overcrowded markets |
| Q3 | Does online ordering improve ratings? | Measure online order feature ROI |
| Q4 | Does table booking correlate with higher ratings? | Measure table booking feature ROI |
| Q5 | What price range delivers the best satisfaction? | Optimal pricing segment strategy |
| Q6 | How do pricing segments compare overall? | Segment-level benchmarking |
| Q7 | Which cuisines are most common in Bangalore? | Market saturation by cuisine |
| Q8 | Which cuisines receive the highest average ratings? | Cuisines to promote on platform |
| Q9 | Which cuisines perform well with fewer restaurants? | Niche market opportunities |
| Q10 | What is the relationship between cost and rating? | Does premium price mean better ratings? |
| Q11 | Which locations are ideal for premium onboarding? | Premium expansion targeting |
| Q12 | Which areas show high demand but low ratings? | Quality improvement priorities |
| Q13 | Do restaurants with both features perform better? | Bundled feature adoption impact |

---

## Installation & Setup

### Prerequisites

- Python 3.10 or higher
- Git

### Steps

1. Clone the repository:
   ```
   bash git clone 
   https://github.com/HariKumaran-369/Uber-Eats-Bangalore__Restaurant-Intelligence-Decision-Support-Systems

   ```

2. (Recommended) Create a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Place the dataset files in the `data/` folder:
   ```
   data/uber_eats_data.csv
   data/orders.json
   ```

---

## Workflow — How to Run This Project

**Run the scripts this exact order**

### Step 1 — Clean the data

```bash
python clean_data.py
```

Loads `data/uber_eats_data.csv`, cleans all columns, engineers the `price_segment` and `rating_category` features, and saves a verified clean dataset.

### Step 2 — Build the database

```bash
python database.py
```

Creates `uber_eats.db` (SQLite), creates the `restaurants` and `orders` tables, and inserts all cleaned data. Prints a verification summary on completion.

### Step 3 — Test SQL queries (optional)

```bash
python queries.py
```

Runs all 15 business questions and prints results to the terminal. Useful for verifying SQL logic before launching the app.

### Step 4 — Launch the web application

```bash
streamlit run app.py
```

Opens the app in your browser at `http://localhost:8501`.

---

## Application Pages

### 🏠 Dashboard
- Six sidebar filters: Location, Price Segment, Online Order, Table Booking, Minimum Rating, Minimum Votes
- All filters dynamically build a SQL `WHERE` clause — no Python-level DataFrame filtering
- Displays filtered restaurant table (up to 200 rows) with live summary metrics
- Location breakdown summary table below the main results

### 📊 Business Q&A
- Dropdown with all 15 business questions
- Run a single selected question or all 15 at once
- Each result includes a business insight annotation below the table

### 📦 Order Analytics
- Seven SQL-driven order analyses covering revenue, payment methods, discount impact, high-value orders, monthly trends, and restaurant-level performance


## Future Improvements

- Migrate from SQLite to MySQL for production-scale deployment
- Add a fourth page for cross-dataset joins (restaurants + orders)
- Deploy to Streamlit Community Cloud for public access

---

## Author

**Hari Kumaran**
GitHub: [@HariKumaran-369](https://github.com/HariKumaran-369)
LinkedIn: [https://www.linkedin.com/in/hari-kumaran-369univers/]
Streamlit: [https://uber-eats-bangalorerestaurant-intelligence-decision-support-sy.streamlit.app/]
---

## License

This project is licensed under the MIT License.
