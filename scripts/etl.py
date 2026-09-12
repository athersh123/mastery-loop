import pandas as pd
from pathlib import Path


def clean_dataset(input_file, output_file, source_name):
    print(f"Reading {input_file}")

    df = pd.read_csv(input_file)

    print(f"Original rows: {len(df)}")

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove rows missing important information
    df = df.dropna(
        subset=[
            "learner_id",
            "item_id",
            "skill_id",
            "response",
            "correct",
            "latency_ms"
        ]
    )

    # Convert columns to proper types
    df["learner_id"] = df["learner_id"].astype(str)
    df["item_id"] = df["item_id"].astype(int)
    df["skill_id"] = df["skill_id"].astype(int)
    df["correct"] = df["correct"].astype(int)
    df["latency_ms"] = df["latency_ms"].astype(int)

    # Add dataset source
    df["source"] = source_name

    # Remove duplicate interactions
    df = df.drop_duplicates()

    # Sort for consistent output
    df = df.sort_values(
        by=["learner_id", "item_id"]
    )

    # Create output directory
    Path(output_file).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Save cleaned dataset
    df.to_csv(
        output_file,
        index=False
    )

    print(f"Cleaned rows: {len(df)}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":

    clean_dataset(
        "data/ednet/interactions.csv",
        "data/processed/ednet_clean.csv",
        "ednet"
    )

    clean_dataset(
        "data/assistments/interactions.csv",
        "data/processed/assistments_clean.csv",
        "assistments"
    )

    print("ETL completed successfully!")