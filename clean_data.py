from io import StringIO
import pandas as pd
import ftfy


def load_and_clean():
    cleaned_lines = []

    with open(
        "data/Uber_Eats_data.csv", "r", encoding="utf-8", errors="ignore"
    ) as f:
        header = f.readline()
        cleaned_lines.append(header)

        for line in f:
            stripped_line = line.strip()

            if not stripped_line:
                continue

            if stripped_line.startswith(
                ("+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ",")
            ):
                if cleaned_lines:
                    cleaned_lines[-1] = cleaned_lines[-1].strip() + " " + line
            else:
                cleaned_lines.append(line)

    csv_string_data = "".join(cleaned_lines)
    df = pd.read_csv(StringIO(csv_string_data), on_bad_lines="skip")

    df = df.rename(
        columns={
            "name": "restaurant_name",
            "approx_cost(for two people)": "approx_cost_for_two",
            "listed_in(type)": "listed_in_type",
            "listed_in(city)": "listed_in_city",
        }
    )

    df["restaurant_name"] = df["restaurant_name"].astype(str).str.strip()

    df["restaurant_name"] = df["restaurant_name"].apply(
        lambda x: ftfy.fix_text(str(x))
    )

    df = df[
        ~df["restaurant_name"].str.startswith(
            ("+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
        )
    ]
    df = df[df["restaurant_name"] != "nan"]

    df.drop_duplicates(inplace=True)
    print(f"After removing duplicates: {len(df)}")

    df.dropna(subset=["restaurant_name", "location"], inplace=True)
    df.dropna(how="all", inplace=True)

    df["cuisines"].fillna("Unknown", inplace=True)
    df["rest_type"].fillna("Unknown", inplace=True)
    df["dish_liked"].fillna("Not Available", inplace=True)
    df["phone"].fillna("Not Available", inplace=True)
    df["online_order"].fillna("No", inplace=True)
    df["book_table"].fillna("No", inplace=True)
    df["votes"].fillna(0, inplace=True)

    df["rate"] = (
        df["rate"]
        .astype(str)
        .str.replace("/5", "", regex=False)
        .str.replace("NEW", "", regex=False)
        .str.replace("-", "", regex=False)
        .str.strip()
    )
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    median_rate = df["rate"].median()
    df["rate"].fillna(median_rate, inplace=True)
    df["rate"] = df["rate"].round(1)

    df["approx_cost_for_two"] = (
        df["approx_cost_for_two"]
        .astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False)
        .str.strip()
    )
    df["approx_cost_for_two"] = pd.to_numeric(
        df["approx_cost_for_two"], errors="coerce"
    )
    median_cost = df["approx_cost_for_two"].median()
    df["approx_cost_for_two"].fillna(median_cost, inplace=True)
    df["approx_cost_for_two"] = df["approx_cost_for_two"].astype(int)

    df["votes"] = (
        pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    )

    df["online_order"] = (
        df["online_order"].map({"Yes": 1, "No": 0}).fillna(0).astype(int)
    )
    df["book_table"] = (
        df["book_table"].map({"Yes": 1, "No": 0}).fillna(0).astype(int)
    )

    df["price_segment"] = pd.cut(
        df["approx_cost_for_two"],
        bins=[0, 300, 700, 99999],
        labels=["Low", "Mid", "Premium"],
    )

    df["rating_category"] = pd.cut(
        df["rate"],
        bins=[0, 3.0, 3.5, 4.0, 5.0],
        labels=["Poor", "Average", "Good", "Excellent"],
    )

    df.reset_index(drop=True, inplace=True)

    return df


if __name__ == "__main__":
    df = load_and_clean()

    print("\n── DATA SHAPE ──")
    print(f"Rows (Shape) : {df.shape}")
    print(f"(Total Rows) : {df.shape[0]}")
    print(f"(Total Columns) : {df.shape[1]}")

    df.to_csv("data/uber_eats_cleaned.csv", index=False, lineterminator="\n")
    print("\nuber_clean.csv saved!")
