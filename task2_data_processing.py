# Task2_Data_Processing.py
# Clean JSON data and save as CSV using Pandas

import pandas as pd
import os

#Step 1: Load JSON --------

def load_data():
    file_path = os.path.join("data", "trends_20260410.json")  # update if needed

    df = pd.read_json(file_path)

    print(f"Loaded {len(df)} rows from JSON file.")
    return df


#Step 2: Clean Data --------

def clean_data(df):
    # Remove duplicates based on post_id
    df = df.drop_duplicates(subset="post_id")

    # Drop rows with missing important values
    df = df.dropna(subset=["post_id", "title", "score"])

    # Convert data types
    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Remove low quality stories
    df = df[df["score"] >= 5]

    # Clean title (remove extra spaces)
    df["title"] = df["title"].str.strip()

    print(f"Remaining rows after cleaning: {len(df)}")
    return df


#Step 3: Save CSV --------

def save_csv(df):
    output_path = os.path.join("data", "trends_clean.csv")

    df.to_csv(output_path, index=False)

    print(f"\nSaved {len(df)} rows to {output_path}")

    # Summary: count per category
    print("\nStories per category:")
    print(df["category"].value_counts())


#Actual Run--------

if __name__ == "__main__":
    data = load_data()
    clean_df = clean_data(data)
    save_csv(clean_df)
