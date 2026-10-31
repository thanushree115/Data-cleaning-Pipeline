# Data Cleaning Pipeline for AI Models

A beginner-friendly Python project that converts a messy CSV dataset into a clean, structured dataset that can be used for data analysis and AI/ML workflows.

## Features

- Detects missing values and fills them.
- Removes duplicate records.
- Trims extra spaces.
- Normalizes inconsistent text such as `AI`, `ai`, and `Ai`.
- Standardizes column names.
- Exports a cleaned CSV file.
- Creates a JSON cleaning report.

## Technologies Used

- Python 3
- Pandas
- CSV and JSON

## Project Structure

```text
Data-Cleaning-Pipeline/
├── dataset.csv
├── clean_data.py
├── cleaned_dataset.csv
├── cleaning_report.json
├── requirements.txt
└── README.md
```

`cleaned_dataset.csv` and `cleaning_report.json` are generated when you run the program. The sample generated files are also included in this repository.

## Setup

1. Install Python 3.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Install the required library:

```bash
pip install -r requirements.txt
```

## Run the Project

```bash
python clean_data.py
```

By default, the program reads `dataset.csv` and creates `cleaned_dataset.csv` and `cleaning_report.json`.

You can also choose your own input and output files:

```bash
python clean_data.py --input dataset.csv --output cleaned_dataset.csv
```

To fill missing numeric values with zero instead of the default median strategy:

```bash
python clean_data.py --missing-strategy zero
```

## Sample Dataset

The sample data contains:
- Inconsistent course names (`AI`, `ai`)
- Extra spaces
- A duplicate Alice record
- A missing mark for David

## How Missing Values Are Handled

- Missing numeric values are filled with the column median by default.
- Missing text values are filled with `Unknown`.
- Empty cells are treated as missing values.

For the sample dataset, David's missing mark is filled using the median of the available marks.

## Expected Result

After running the program:
- Duplicate rows are removed.
- Course names use consistent labels.
- Extra spaces are removed.
- Missing values are filled.
- A cleaned CSV and a JSON report are created.

## Future Improvements

- Add an interactive dashboard.
- Support Excel files.
- Add charts showing data quality before and after cleaning.
- Allow users to choose different missing-value strategies for each column.

## Author

Add your name here.

## License

This project is available for learning and educational use.
