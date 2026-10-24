from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "hr_analytics_raw.csv"


def load_data(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")

    df = pd.read_csv(file_path)
    print("Dataset loaded successfully.")

    return df


def inspect_dataset(df):
    print("\n" + "=" * 50)
    print("HR ANALYTICS - DATA UNDERSTANDING")
    print("=" * 50)

    print("\nDATASET DIMENSIONS")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    print("\nFIRST FIVE RECORDS")
    print(df.head())

    print("\nCOLUMN NAMES")
    print(df.columns.tolist())

    print("\nDATA TYPES AND NON-NULL COUNTS")
    df.info()

    print("\nMISSING VALUES AND PERCENTAGES")
    missing_summary = pd.DataFrame({
        "Missing_Count": df.isnull().sum(),
        "Missing_Percentage": (df.isnull().mean() * 100).round(2)
    })
    print(missing_summary)

    print("\nEXACT DUPLICATE ROWS")
    print(df.duplicated().sum())

    print("\nROWS INVOLVED IN DUPLICATE GROUPS")
    print(df.duplicated(keep=False).sum())

    print("\nNUMERICAL DESCRIPTIVE STATISTICS")
    print(df.describe())


def inspect_employee_ids(df):
    if "EmployeeID" not in df.columns:
        return

    print("\nEMPLOYEE ID VALIDATION")
    print("Unique Employee IDs:", df["EmployeeID"].nunique())
    print("Missing Employee IDs:", df["EmployeeID"].isna().sum())
    print("Duplicate Employee ID entries:", df["EmployeeID"].duplicated().sum())


def inspect_categorical_columns(df):
    columns = [
        "Gender",
        "Department",
        "JobRole",
        "Attrition",
        "Overtime",
        "JobSatisfaction",
        "PerformanceRating",
        "EducationLevel"
    ]

    print("\nCATEGORICAL DISTRIBUTIONS")

    for column in columns:
        if column in df.columns:
            print(f"\n{column} Distribution")
            print(df[column].value_counts(dropna=False))


def inspect_numeric_columns(df):
    columns = ["Age", "MonthlyIncome", "YearsAtCompany"]

    print("\nNUMERIC COLUMN VALIDATION")

    for column in columns:
        if column not in df.columns:
            continue

        original_values = df[column].astype("string").str.strip()
        cleaned_values = original_values.copy()

        if column == "MonthlyIncome":
            cleaned_values = cleaned_values.str.replace(
                r"[₹,]|\s*INR\b", "", regex=True
            )
        elif column == "Age":
            cleaned_values = cleaned_values.str.replace(
                r"\s*years\s*", "", regex=True
            )

        numeric_values = pd.to_numeric(cleaned_values, errors="coerce")

        invalid_mask = original_values.notna() & numeric_values.isna()

        print(f"\n{column}")
        print("Missing values:", df[column].isna().sum())

        print("Values that cannot be converted to numbers:")
        print(original_values[invalid_mask].value_counts().to_dict())

        print("Numeric summary:")
        print(numeric_values.describe())

        print("Value distribution:")
        print(numeric_values.value_counts(dropna=False).sort_index().head(20))

        if column == "Age":
            unusual_ages = numeric_values[numeric_values.isin([15, 120])]
            print("Ages flagged for review:", unusual_ages.tolist())

        elif column == "MonthlyIncome":
            print("Negative income values:", int((numeric_values < 0).sum()))
            print(
                "Income values above 100000:",
                int((numeric_values > 100000).sum())
            )

        elif column == "YearsAtCompany":
            print("Negative tenure values:", int((numeric_values < 0).sum()))


def inspect_category_values(df):
    expected_categories = {
        "JobSatisfaction": {"low", "medium", "high", "very high"},
        "Attrition": {"yes", "no"},
        "Overtime": {"yes", "no"}
    }

    print("\nCATEGORY VALIDATION")

    for column, expected in expected_categories.items():
        if column not in df.columns:
            continue

        normalized = (
            df[column]
            .astype("string")
            .str.strip()
            .str.casefold()
        )

        invalid_mask = df[column].notna() & ~normalized.isin(expected)

        print(f"\n{column}")
        print("Unexpected values:")
        print(df.loc[invalid_mask, column].value_counts().to_dict())
        print("Missing values:", df[column].isna().sum())


def main():
    df = load_data(DATA_PATH)

    inspect_dataset(df)
    inspect_employee_ids(df)
    inspect_categorical_columns(df)
    inspect_numeric_columns(df)
    inspect_category_values(df)

    print("\n" + "=" * 50)
    print("DATA UNDERSTANDING COMPLETED")
    print("=" * 50)


if __name__ == "__main__":
    main()

