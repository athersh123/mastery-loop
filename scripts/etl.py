
import pandas as pd
from pathlib import Path

REQUIRED_COLUMNS = [
    "learner_id",
    "item_id",
    "skill_id",
    "response",
    "correct",
    "latency_ms",
]


def clean_dataset(input_file, output_file, source_name):
    print(f"\nReading {input_file}")
    df = pd.read_csv(input_file)

    original_rows = len(df)
    print(f"Original rows: {original_rows}")

    # Remove completely empty rows
    df = df.dropna(how="all")

    # Validate the input schema
    missing_columns = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]
    if missing_columns:
        raise ValueError(
            f"{source_name}: missing columns: {missing_columns}"
        )

    # Remove rows missing required values
    df = df.dropna(subset=REQUIRED_COLUMNS).copy()

    # Validate numeric fields before conversion
    numeric_columns = [
        "item_id",
        "skill_id",
        "correct",
        "latency_ms",
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Drop rows with invalid numeric values
    df = df.dropna(subset=numeric_columns).copy()

    # Reject fractional values for integer fields
    integer_columns = numeric_columns
    for col in integer_columns:
        df = df[df[col] % 1 == 0]

    # Normalize integer types
    for col in integer_columns:
        df[col] = df[col].astype("int64")

    # Normalize learner IDs and reject empty IDs
    df["learner_id"] = df["learner_id"].astype(str).str.strip()
    df = df[df["learner_id"] != ""].copy()

    # Validate domain constraints
    df = df[df["item_id"] >= 0]
    df = df[df["skill_id"] >= 0]
    df = df[df["correct"].isin([0, 1])]
    df = df[df["latency_ms"] >= 0]

    # Keep response values as strings, without inventing mappings
    df["response"] = df["response"].astype(str).str.strip()
    df = df[df["response"] != ""].copy()

    # Record source and remove exact duplicate rows
    df["source"] = source_name
    df = df.drop_duplicates()

    # No timestamp exists, so do not claim chronological order.
    # Sort deterministically using available columns.
    df = df.sort_values(
        ["learner_id", "item_id", "skill_id"],
        kind="stable",
    ).reset_index(drop=True)

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Rows read: {original_rows}")
    print(f"Rows retained: {len(df)}")
    print(f"Rows removed: {original_rows - len(df)}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    clean_dataset(
        "data/ednet/interactions.csv",
        "data/processed/ednet_clean.csv",
        "ednet",
    )

    clean_dataset(
        "data/assistments/interactions.csv",
        "data/processed/assistments_clean.csv",
        "assistments",
    )

    print("\nETL completed successfully!")
