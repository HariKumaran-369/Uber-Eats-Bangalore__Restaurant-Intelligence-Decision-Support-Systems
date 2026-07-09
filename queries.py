import sqlite3
import pandas as pd

DATABASE = "uber_eats.db"


def run_query(sql: str) -> pd.DataFrame:
    """Execute any SQL query and return results as a DataFrame."""
    conn = sqlite3.connect(DATABASE)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


def q1_top_rated_locations():
    return run_query("""
        SELECT
            location,
            ROUND(AVG(rate), 2)  AS avg_rating,
            COUNT(*)              AS total_restaurants
        FROM restaurants
        GROUP BY location
        HAVING COUNT(*) >= 10
        ORDER BY avg_rating DESC
        LIMIT 10
    """)


def q2_oversaturated_locations():
    return run_query("""
        SELECT
            location,
            COUNT(*) AS restaurant_count
        FROM restaurants
        GROUP BY location
        ORDER BY restaurant_count DESC
        LIMIT 10
    """)


def q3_online_order_vs_rating():
    return run_query("""
        SELECT
            CASE WHEN online_order = 1
                     THEN 'Yes' ELSE 'No'
            END AS online_order,
            ROUND(AVG(rate), 2)  AS avg_rating,
            COUNT(*)              AS restaurant_count
        FROM restaurants
        GROUP BY online_order
        ORDER BY avg_rating DESC
    """)


def q4_table_booking_vs_rating():
    return run_query("""
        SELECT
            CASE WHEN book_table = 1 THEN 'Yes' ELSE 'No' END AS book_table,
            ROUND(AVG(rate), 2)  AS avg_rating,
            COUNT(*)              AS restaurant_count
        FROM restaurants
        GROUP BY book_table
        ORDER BY avg_rating DESC
    """)


def q5_price_vs_satisfaction():
    return run_query("""
        SELECT
            price_segment,
            ROUND(AVG(rate), 2)           AS avg_rating,
            ROUND(AVG(approx_cost_for_two), 0) AS avg_cost,
            COUNT(*)                       AS restaurant_count
        FROM restaurants
        WHERE price_segment IS NOT NULL
        GROUP BY price_segment
        ORDER BY avg_rating DESC
    """)


def q6_pricing_segment_performance():
    return run_query("""
        SELECT
            price_segment,
            COUNT(*)              AS total_restaurants,
            ROUND(AVG(rate), 2)  AS avg_rating,
            ROUND(MIN(rate), 2)  AS min_rating,
            ROUND(MAX(rate), 2)  AS max_rating,
            SUM(votes)            AS total_votes
        FROM restaurants
        WHERE price_segment IS NOT NULL
        GROUP BY price_segment
        ORDER BY avg_rating DESC
    """)


def q7_most_common_cuisines():
    return run_query("""
        SELECT
            cuisines,
            COUNT(*) AS restaurant_count
        FROM restaurants
        WHERE cuisines != 'Unknown'
        GROUP BY cuisines
        ORDER BY restaurant_count DESC
        LIMIT 15
    """)


def q8_top_rated_cuisines():
    return run_query("""
        SELECT
            cuisines,
            ROUND(AVG(rate), 2)  AS avg_rating,
            COUNT(*)              AS restaurant_count,
            SUM(votes)            AS total_votes
        FROM restaurants
        WHERE cuisines != 'Unknown'
        GROUP BY cuisines
        HAVING COUNT(*) >= 5
        ORDER BY avg_rating DESC
        LIMIT 10
    """)


def q9_niche_cuisine_opportunities():
    return run_query("""
        SELECT
            cuisines,
            COUNT(*)              AS restaurant_count,
            ROUND(AVG(rate), 2)  AS avg_rating
        FROM restaurants
        WHERE cuisines != 'Unknown'
        GROUP BY cuisines
        HAVING COUNT(*) BETWEEN 3 AND 15
            AND AVG(rate) >= 4.0
        ORDER BY avg_rating DESC
        LIMIT 10
    """)


def q10_cost_vs_rating():
    return run_query("""
        SELECT
            price_segment,
            ROUND(AVG(approx_cost_for_two), 0) AS avg_cost,
            ROUND(AVG(rate), 2)                 AS avg_rating,
            COUNT(*)                             AS restaurant_count
        FROM restaurants
        WHERE price_segment IS NOT NULL
        GROUP BY price_segment
        ORDER BY avg_cost ASC
    """)


def q11_premium_onboarding_locations():
    return run_query("""
        SELECT
            location,
            ROUND(AVG(rate), 2)                 AS avg_rating,
            ROUND(AVG(approx_cost_for_two), 0)  AS avg_cost,
            COUNT(*)                             AS premium_restaurants
        FROM restaurants
        WHERE price_segment = 'Premium'
        GROUP BY location
        HAVING COUNT(*) >= 5
        ORDER BY avg_rating DESC
        LIMIT 10
    """)


def q12_high_demand_low_quality():
    return run_query("""
        SELECT
            location,
            COUNT(*)              AS restaurant_count,
            ROUND(AVG(rate), 2)  AS avg_rating,
            SUM(votes)            AS total_votes
        FROM restaurants
        GROUP BY location
        HAVING COUNT(*) >= 20
            AND AVG(rate) < 3.8
        ORDER BY restaurant_count DESC
    """)


if __name__ == "__main__":
    questions = {
        "Q1  Top rated locations": q1_top_rated_locations,
        "Q2  Over-saturated locations": q2_oversaturated_locations,
        "Q3  Online order vs rating": q3_online_order_vs_rating,
        "Q4  Table booking vs rating": q4_table_booking_vs_rating,
        "Q5  Price range vs satisfaction": q5_price_vs_satisfaction,
        "Q6  Pricing segment performance": q6_pricing_segment_performance,
        "Q7  Most common cuisines": q7_most_common_cuisines,
        "Q8  Top rated cuisines": q8_top_rated_cuisines,
        "Q9  Niche cuisine opportunities": q9_niche_cuisine_opportunities,
        "Q10 Cost vs rating": q10_cost_vs_rating,
        "Q11 Premium onboarding locations": q11_premium_onboarding_locations,
        "Q12 High demand low quality": q12_high_demand_low_quality,
    }

    for title, func in questions.items():
        print(f"\n{'='*55}")
        print(f"  {title}")
        print("=" * 55)
        result = func()
        print(result.to_string(index=False))
