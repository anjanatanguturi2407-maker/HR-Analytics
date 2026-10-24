from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "hr_analytics_raw.csv"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "hr_analytics_clean.csv"

CATEGORICAL_COLUMNS = [
    "Gender",
    "Department",
    "JobRole",
    "JobSatisfaction",
    "Overtime",
    "PerformanceRating",
    "EducationLevel",
]

DEPARTMENT_MAPPING = {
    "ops": "Operations",
    "operations": "Operations",
    "it": "IT",
    "i.t.": "IT",
    "r&d": "Research & Development",
    "research and development": "Research & Development",
    "research & development": "Research & Development",
    "hr": "Human Resources",
    "human resources": "Human Resources",
    "cust support": "Customer Support",
    "customer service": "Customer Support",
    "customer support": "Customer Support",
    "sale": "Sales",
    "sales": "Sales",
    "finance": "Finance",
    "unknown": "Unknown",
}

ATTRITION_MAPPING = {
    "yes": "Yes",
    "y": "Yes",
    "no": "No",
    "n": pd.NA,
    "false": "No",
    "true": "Yes",
}

OVERTIME_MAPPING = {
    "yes": "Yes",
    "y": "Yes",
    "true": "Yes",
    "no": "No",
    "n": "No",
    "false": "No",
}

SATISFACTION_MAPPING = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "very high": "Very High",
}

PERFORMANCE_MAPPING = {
    "needs improvement": "Needs Improvement",
    "meets expectations": "Meets Expectations",
    "exceeds expectations": "Exceeds Expectations",
}

EDUCATION_MAPPING = {
    "high school": "High School",
    "bachelor's": "Bachelor's",
    "master's": "Master's",
    "phd": "PhD",
}


def load_data(file_path):
    if not file_path.exists():
        raise FileNotFoundError(f"Input dataset not found: {file_path}")

    return pd.read_csv(file_path)


def remove_duplicate_rows(df):
    original_count = len(df)
    cleaned_df = df.drop_duplicates().copy()
    removed_count = original_count - len(cleaned_df)

    print(f"Duplicate rows removed: {removed_count}")
    print(f"Rows remaining: {len(cleaned_df)}")

    return cleaned_df


def standardize_text_column(series):
    return series.astype("string").str.strip()


def standardize_categorical_values(df):
    for column in CATEGORICAL_COLUMNS:
        if column in df.columns:
            df[column] = standardize_text_column(df[column])

    if "Gender" in df.columns:
        df["Gender"] = df["Gender"].str.title()

    if "Department" in df.columns:
        normalized = df["Department"].str.casefold()
        df["Department"] = normalized.map(DEPARTMENT_MAPPING).fillna(
            df["Department"].str.title()
        )
        df.loc[df["Department"].str.casefold() == "unknown", "Department"] = "Unknown"

    if "Attrition" in df.columns:
        normalized = df["Attrition"].str.casefold()
        df["Attrition"] = normalized.map(ATTRITION_MAPPING).where(
            normalized.isin(ATTRITION_MAPPING), df["Attrition"]
        )

    if "Overtime" in df.columns:
        normalized = df["Overtime"].str.casefold()
        df["Overtime"] = normalized.map(OVERTIME_MAPPING).where(
            normalized.isin(OVERTIME_MAPPING), df["Overtime"]
        )

    if "JobSatisfaction" in df.columns:
        normalized = df["JobSatisfaction"].str.casefold()
        df["JobSatisfaction"] = normalized.map(SATISFACTION_MAPPING).where(
            normalized.isin(SATISFACTION_MAPPING), df["JobSatisfaction"]
        )

    if "PerformanceRating" in df.columns:
        normalized = df["PerformanceRating"].str.casefold()
        df["PerformanceRating"] = normalized.map(PERFORMANCE_MAPPING).where(
            normalized.isin(PERFORMANCE_MAPPING), df["PerformanceRating"]
        )

    if "EducationLevel" in df.columns:
        normalized = df["EducationLevel"].str.casefold()
        df["EducationLevel"] = normalized.map(EDUCATION_MAPPING).where(
            normalized.isin(EDUCATION_MAPPING), df["EducationLevel"]
        )

    return df


def convert_numeric_columns(df):
    if "Age" in df.columns:
        age_values = (
            df["Age"]
            .astype("string")
            .str.strip()
            .str.replace(r"\s*years\s*", "", regex=True)
        )
        df["Age"] = pd.to_numeric(age_values, errors="coerce")
        df.loc[(df["Age"] < 18) | (df["Age"] > 60), "Age"] = pd.NA

    if "MonthlyIncome" in df.columns:
        income_values = (
            df["MonthlyIncome"]
            .astype("string")
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace(r"\s*INR\b", "", regex=True)
            .str.strip()
        )
        df["MonthlyIncome"] = pd.to_numeric(income_values, errors="coerce")
        df.loc[df["MonthlyIncome"] < 0, "MonthlyIncome"] = pd.NA

    if "YearsAtCompany" in df.columns:
        tenure_values = (
            df["YearsAtCompany"]
            .astype("string")
            .str.strip()
            .str.casefold()
            .replace({
                "five": "5",
                "3 yrs": "3",
                "forty": "40",
            })
        )
        df["YearsAtCompany"] = pd.to_numeric(tenure_values, errors="coerce")
        df.loc[df["YearsAtCompany"] < 0, "YearsAtCompany"] = pd.NA

    return df


def handle_missing_values(df):
    categorical_columns = [
        "Gender",
        "Department",
        "JobRole",
        "JobSatisfaction",
        "Overtime",
        "PerformanceRating",
        "EducationLevel",
    ]

    for column in categorical_columns:
        if column in df.columns:
            df[column] = df[column].fillna("Unknown")

    for column in ["Age", "MonthlyIncome", "YearsAtCompany"]:
        if column in df.columns:
            median_value = df[column].median()
            if pd.notna(median_value):
                df[column] = df[column].fillna(median_value)
                print(f"{column} missing values filled with median: {median_value:g}")

    return df


def validate_data(df):
    print("\nFINAL DATA QUALITY REPORT")
    print("-" * 40)
    print("Dataset shape:", df.shape)
    print("Duplicate rows:", df.duplicated().sum())

    if "EmployeeID" in df.columns:
        print("Missing EmployeeIDs:", df["EmployeeID"].isna().sum())
        print("Duplicate EmployeeIDs:", df["EmployeeID"].duplicated().sum())

    print("\nMissing values by column:")
    print(df.isna().sum())

    print("\nData types:")
    print(df.dtypes)

    if "MonthlyIncome" in df.columns:
        print("\nMonthlyIncome values equal to 999999:")
        print(int(df["MonthlyIncome"].eq(999999).sum()))

    if "YearsAtCompany" in df.columns:
        print("\nMaximum YearsAtCompany:")
        print(df["YearsAtCompany"].max())


def save_data(df, file_path):
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)
    print(f"\nCleaned dataset saved to: {file_path}")


def main():
    df = load_data(RAW_DATA_PATH)

    print("Original dataset shape:", df.shape)

    df = remove_duplicate_rows(df)
    df = standardize_categorical_values(df)
    df = convert_numeric_columns(df)
    df = handle_missing_values(df)

    validate_data(df)
    save_data(df, PROCESSED_DATA_PATH)

    print("\nData cleaning completed successfully.")


if __name__ == "__main__":
    main()
