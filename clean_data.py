"""
Data Cleaning Pipeline for AI Models
------------------------------------
Cleans a CSV dataset by:
1. Standardizing column names and text
2. Detecting and handling missing values
3. Removing duplicate rows
4. Normalizing inconsistent text
5. Saving a cleaned CSV and a cleaning report

Usage:
    python clean_data.py
    python clean_data.py --input dataset.csv --output cleaned_dataset.csv
    python clean_data.py --input dataset.csv --output cleaned_dataset.csv --missing-strategy median
"""

import argparse
import json
import re
from pathlib import Path

import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Make column names lowercase, with underscores instead of spaces."""
    df = df.copy()
    df.columns = [
        re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", str(col).strip().lower())).strip("_")
        for col in df.columns
    ]
    return df


def normalize_text(df: pd.DataFrame) -> pd.DataFrame:
    """Trim extra spaces and standardize text capitalization."""
    df = df.copy()
    for column in df.select_dtypes(include=["object", "string"]).columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

        # Normalize common course-name variations, e.g. AI, ai, Ai -> Ai.
        if column == "course":
            df[column] = df[column].str.casefold().replace({
                "ai": "Artificial Intelligence",
                "artificial intelligence": "Artificial Intelligence",
                "data science": "Data Science",
                "python": "Python",
                "computer science": "Computer Science",
            })
        elif column == "name":
            df[column] = df[column].str.title()

    return df


def handle_missing_values(df: pd.DataFrame, strategy: str = "auto") -> tuple[pd.DataFrame, dict]:
    """
    Handle missing values.
    - Numeric columns: median (or zero when median is unavailable)
    - Text columns: 'Unknown'
    - Empty strings are treated as missing values
    """
    df = df.copy()
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    missing_before = {str(k): int(v) for k, v in df.isna().sum().items() if v > 0}

    for column in df.columns:
        if not df[column].isna().any():
            continue

        if pd.api.types.is_numeric_dtype(df[column]):
            if strategy == "zero":
                fill_value = 0
            else:
                median = df[column].median()
                fill_value = 0 if pd.isna(median) else median
            df[column] = df[column].fillna(fill_value)
        else:
            df[column] = df[column].fillna("Unknown")

    return df, missing_before


def clean_dataset(input_path: Path, output_path: Path, missing_strategy: str = "auto") -> dict:
    """Run the complete cleaning pipeline and save results."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)
    original_rows = len(df)
    original_columns = len(df.columns)

    df = standardize_column_names(df)
    df = normalize_text(df)
    df, missing_before = handle_missing_values(df, missing_strategy)

    duplicates_removed = int(df.duplicated().sum())
    df = df.drop_duplicates().reset_index(drop=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    report = {
        "input_file": str(input_path),
        "output_file": str(output_path),
        "rows_before_cleaning": original_rows,
        "rows_after_cleaning": len(df),
        "columns": original_columns,
        "duplicate_rows_removed": duplicates_removed,
        "missing_values_found": missing_before,
        "missing_values_remaining": int(df.isna().sum().sum()),
        "cleaning_steps": [
            "Standardized column names",
            "Trimmed extra spaces and normalized text",
            "Handled missing values",
            "Removed duplicate rows",
            "Saved cleaned CSV file",
        ],
    }

    report_path = output_path.with_name("cleaning_report.json")
    report_path.write_text(json.dumps(report, indent=4), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description="Clean a messy CSV dataset.")
    parser.add_argument("--input", default="dataset.csv", help="Path to input CSV file")
    parser.add_argument("--output", default="cleaned_dataset.csv", help="Path to output CSV file")
    parser.add_argument(
        "--missing-strategy",
        choices=["auto", "zero"],
        default="auto",
        help="How to fill missing numeric values: median (auto) or zero",
    )
    args = parser.parse_args()

    try:
        report = clean_dataset(Path(args.input), Path(args.output), args.missing_strategy)
        print("\nDATA CLEANING COMPLETED")
        print("----------------------")
        print(f"Rows before cleaning : {report['rows_before_cleaning']}")
        print(f"Rows after cleaning  : {report['rows_after_cleaning']}")
        print(f"Duplicates removed   : {report['duplicate_rows_removed']}")
        print(f"Missing values found : {sum(report['missing_values_found'].values())}")
        print(f"Missing values left  : {report['missing_values_remaining']}")
        print(f"\nCleaned file saved   : {args.output}")
        print("Report saved         : cleaning_report.json")
    except Exception as error:
        raise SystemExit(f"Error: {error}")


if __name__ == "__main__":
    main()
