import sqlite3
import pandas as pd
import json

DB_PATH = "uber_eats.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_restaurants_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS restaurants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_name TEXT,
            online_order INTEGER,
            book_table INTEGER,
            rate REAL,
            votes INTEGER,
            phone TEXT,
            location TEXT,
            rest_type TEXT,
            dish_liked TEXT,
            cuisines TEXT,
            approx_cost_for_two INTEGER,
            listed_in_type TEXT,
            listed_in_city TEXT,
            price_segment TEXT,
            rating_category TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_orders_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            restaurant_name TEXT,
            order_date TEXT,
            order_value REAL,
            discount_used TEXT,
            payment_method TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_restaurants(csv_file="data/uber_eats_cleaned.csv"):
    df = pd.read_csv(csv_file)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM restaurants")

    rows = [
        (
            row["restaurant_name"],
            int(row["online_order"]),
            int(row["book_table"]),
            float(row["rate"]),
            int(row["votes"]),
            row["phone"],
            row["location"],
            row["rest_type"],
            row["dish_liked"],
            row["cuisines"],
            int(row["approx_cost_for_two"]),
            row["listed_in_type"],
            row["listed_in_city"],
            row["price_segment"],
            row["rating_category"],
        )
        for _, row in df.iterrows()
    ]

    cursor.executemany(
        """
        INSERT INTO restaurants (
            restaurant_name, online_order, book_table, rate, votes, phone,
            location, rest_type, dish_liked, cuisines, approx_cost_for_two,
            listed_in_type, listed_in_city, price_segment, rating_category
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
        rows,
    )

    conn.commit()
    conn.close()
    print(f"{len(df)} restaurant rows inserted into DB")


def insert_orders(json_file="data/orders.json"):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    df_orders = pd.DataFrame(data)
    df_orders.columns = df_orders.columns.str.strip().str.lower()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM orders")

    rows = [
        (
            row["order_id"],
            row["restaurant_name"],
            row["order_date"],
            float(row["order_value"]),
            row["discount_used"],
            row["payment_method"],
        )
        for _, row in df_orders.iterrows()
    ]

    cursor.executemany(
        """
        INSERT OR REPLACE INTO orders (
            order_id, restaurant_name, order_date,
            order_value, discount_used, payment_method
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        rows,
    )

    conn.commit()
    conn.close()
    print(f"{len(df_orders)} order rows inserted into DB")


def verify_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("\nAvailable tables:")
    for t in tables:
        print(t[0])

    cursor.execute("SELECT COUNT(*) FROM restaurants")
    rest_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]

    print("\n--- Database Verification ---")
    print("Restaurants rows:", rest_count)
    print("Orders rows:", order_count)

    cursor.execute("SELECT * FROM restaurants LIMIT 3")
    print("\nSample restaurants:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM orders LIMIT 3")
    print("\nSample orders:")
    for row in cursor.fetchall():
        print(row)

    conn.close()


if __name__ == "__main__":
    create_restaurants_table()
    create_orders_table()
    insert_restaurants()
    insert_orders()
    verify_database()
