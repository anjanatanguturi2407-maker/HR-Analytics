from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "hr_analytics_clean.csv"
IMAGE_PATH = PROJECT_ROOT / "images"


def load_data(file_path):
    return pd.read_csv(file_path)


def prepare_analysis_data(df):
    df = df.copy()
    df["MonthlyIncome_EDA"] = df["MonthlyIncome"].replace(999999, float("nan"))

    df_valid = df[df["Attrition"].isin(["Yes", "No"])].copy()

    df_valid["AgeGroup"] = pd.cut(
        df_valid["Age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=["Under 25", "25–34", "35–44", "45–54", "55+"],
        right=False
    )

    return df, df_valid


def save_figure(file_name):
    IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(IMAGE_PATH / file_name, dpi=300, bbox_inches="tight")
    plt.close()


def inspect_dataset(df):
    print("Dataset Shape:", df.shape)
    print("\nFirst Five Rows:")
    print(df.head())
    print("\nDataset Information:")
    df.info()
    print("\nStatistical Summary:")
    print(df.describe(include="all"))
    print("\nMissing Values:")
    print(df.isnull().sum())
    print("\nDuplicate Rows:", df.duplicated().sum())


def plot_attrition_distribution(df):
    counts = df["Attrition"].dropna().value_counts()

    plt.figure(figsize=(7, 5))
    sns.barplot(x=counts.index, y=counts.values)
    plt.title("Employee Attrition Distribution")
    plt.xlabel("Employee Attrition")
    plt.ylabel("Number of Employees")
    save_figure("attrition_distribution.png")


def plot_department_analysis(df):
    plt.figure(figsize=(10, 7))
    sns.countplot(data=df, x="Department", hue="Attrition")
    plt.title("Department-Wise Employee Attrition")
    plt.xlabel("Department")
    plt.ylabel("Number of Employees")
    plt.xticks(rotation=45)
    save_figure("department_attrition_counts.png")

    df_valid = df.dropna(subset=["Attrition"])

    department_rate = (
        df_valid.groupby("Department")["Attrition"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 7))
    sns.barplot(x=department_rate.index, y=department_rate.values)
    plt.title("Department-Wise Attrition Rate")
    plt.xlabel("Department")
    plt.ylabel("Attrition Rate (%)")
    plt.xticks(rotation=45)
    save_figure("department_attrition_rate.png")

    print("\nDepartment-Wise Attrition Rate (%):")
    print(department_rate.round(2))

    return department_rate


def plot_job_role_analysis(df):
    df_valid = df[df["Attrition"].isin(["Yes", "No"])]

    plt.figure(figsize=(12, 6))
    sns.countplot(data=df_valid, y="JobRole", hue="Attrition")
    plt.title("Job Role-Wise Employee Attrition")
    plt.xlabel("Number of Employees")
    plt.ylabel("Job Role")
    save_figure("job_role_attrition_counts.png")

    job_role_rate = (
        df_valid.groupby("JobRole")["Attrition"]
        .apply(lambda x: (x == "Yes").mean() * 100)
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 8))
    sns.barplot(x=job_role_rate.values, y=job_role_rate.index)
    plt.title("Job Role-Wise Attrition Rate")
    plt.xlabel("Attrition Rate (%)")
    plt.ylabel("Job Role")
    save_figure("job_role_attrition_rate.png")

    print("\nJob Role-Wise Attrition Rate (%):")
    print(job_role_rate.round(2))

    return job_role_rate


def plot_age_analysis(df, df_valid):
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="Age", bins=15)
    plt.title("Age Distribution of Employees")
    plt.xlabel("Age")
    plt.ylabel("Number of Employees")
    save_figure("age_distribution.png")

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_valid, x="Attrition", y="Age")
    plt.title("Age vs Employee Attrition")
    plt.xlabel("Attrition")
    plt.ylabel("Age")
    save_figure("age_vs_attrition.png")

    age_rate = (
        df_valid.groupby("AgeGroup", observed=False)["Attrition"]
        .apply(lambda x: (x == "Yes").mean() * 100)
    )

    print("\nAge-Group-Wise Attrition Rate (%):")
    print(age_rate.round(2))

    plt.figure(figsize=(9, 5))
    sns.barplot(x=age_rate.index, y=age_rate.values)
    plt.title("Age Group vs Employee Attrition Rate")
    plt.xlabel("Age Group")
    plt.ylabel("Attrition Rate (%)")
    save_figure("age_group_attrition_rate.png")

    return age_rate


def plot_income_analysis(df, df_valid):
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="MonthlyIncome", bins=20)
    plt.title("Monthly Income Distribution")
    plt.xlabel("Monthly Income")
    plt.ylabel("Number of Employees")
    save_figure("monthly_income_distribution_all.png")

    income_filtered = df[df["MonthlyIncome"] < 100000]

    plt.figure(figsize=(8, 5))
    sns.histplot(data=income_filtered, x="MonthlyIncome", bins=20)
    plt.title("Monthly Income Distribution Below 100,000")
    plt.xlabel("Monthly Income")
    plt.ylabel("Number of Employees")
    save_figure("monthly_income_distribution_filtered.png")

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_valid, x="Attrition", y="MonthlyIncome")
    plt.title("Monthly Income vs Employee Attrition")
    plt.xlabel("Attrition")
    plt.ylabel("Monthly Income")
    save_figure("income_vs_attrition_all.png")

    income_valid = df_valid[df_valid["MonthlyIncome"] < 100000]

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=income_valid, x="Attrition", y="MonthlyIncome")
    plt.title("Monthly Income vs Employee Attrition Below 100,000")
    plt.xlabel("Attrition")
    plt.ylabel("Monthly Income")
    save_figure("income_vs_attrition_filtered.png")

    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="MonthlyIncome_EDA", bins=20)
    plt.title("Monthly Income Distribution Excluding Flagged Values")
    plt.xlabel("Monthly Income")
    plt.ylabel("Number of Employees")
    save_figure("monthly_income_distribution_excluding_flagged.png")

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_valid, x="Attrition", y="MonthlyIncome_EDA")
    plt.title("Monthly Income vs Attrition Excluding Flagged Values")
    plt.xlabel("Attrition")
    plt.ylabel("Monthly Income")
    save_figure("income_vs_attrition_excluding_flagged.png")

    print("\nMonthly Income Summary:")
    print(df["MonthlyIncome"].describe())

    print("\nMonthly Income Summary Excluding Flagged Values:")
    print(df["MonthlyIncome_EDA"].describe())

    print("\nFlagged Income Records:")
    print(df[df["MonthlyIncome"] == 999999])


def plot_tenure_analysis(df, df_valid):
    plt.figure(figsize=(8, 5))
    sns.histplot(data=df, x="YearsAtCompany", bins=15)
    plt.title("Years at Company Distribution")
    plt.xlabel("Years at Company")
    plt.ylabel("Number of Employees")
    save_figure("years_at_company_distribution.png")

    plt.figure(figsize=(8, 5))
    sns.boxplot(data=df_valid, x="Attrition", y="YearsAtCompany")
    plt.title("Years at Company vs Employee Attrition")
    plt.xlabel("Attrition")
    plt.ylabel("Years at Company")
    save_figure("tenure_vs_attrition.png")


def plot_categorical_analysis(df):
    columns = [
        ("JobSatisfaction", "Job Satisfaction vs Employee Attrition", "job_satisfaction_attrition.png", 0),
        ("Overtime", "Overtime vs Employee Attrition", "overtime_attrition.png", 0),
        ("EducationLevel", "Education Level vs Employee Attrition", "education_attrition.png", 30),
        ("PerformanceRating", "Performance Rating vs Employee Attrition", "performance_attrition.png", 10),
        ("Gender", "Gender vs Employee Attrition", "gender_attrition.png", 0)
    ]

    df_valid = df.dropna(subset=["Attrition"])

    for column, title, file_name, rotation in columns:
        plt.figure(figsize=(9, 5))
        sns.countplot(data=df_valid, x=column, hue="Attrition")
        plt.title(title)
        plt.xlabel(column)
        plt.ylabel("Number of Employees")

        if rotation:
            plt.xticks(rotation=rotation)

        save_figure(file_name)


def print_crosstab_summaries(df):
    print("\nAttrition Counts:")
    print(df["Attrition"].value_counts(dropna=False))

    for column in [
        "Overtime",
        "JobSatisfaction",
        "Gender",
        "EducationLevel",
        "PerformanceRating"
    ]:
        print(f"\n{column} vs Attrition:")
        print(pd.crosstab(df[column], df["Attrition"]))


def plot_correlation_heatmap(df):
    columns = ["Age", "MonthlyIncome_EDA", "YearsAtCompany"]

    plt.figure(figsize=(8, 5))
    sns.heatmap(df[columns].corr(), annot=True, cmap="Reds", fmt=".2f")
    plt.title("Employee Data Correlation Heatmap")
    save_figure("employee_correlation_heatmap.png")


def print_final_summary(df):
    df_valid = df[df["Attrition"].isin(["Yes", "No"])]

    total_employees = len(df_valid)
    employees_left = (df_valid["Attrition"] == "Yes").sum()
    employees_stayed = (df_valid["Attrition"] == "No").sum()

    attrition_rate = (
        employees_left / total_employees * 100
        if total_employees > 0
        else 0
    )

    print("\nFinal EDA Summary")
    print("-----------------")
    print("Total Records:", len(df))
    print("Records with Known Attrition:", total_employees)
    print("Employees Who Left:", employees_left)
    print("Employees Who Stayed:", employees_stayed)
    print("Overall Attrition Rate:", round(attrition_rate, 2), "%")
    print("Missing Attrition Labels:", df["Attrition"].isna().sum())
    print("Flagged Income Values:", df["MonthlyIncome_EDA"].isna().sum())


def main():
    df = load_data(DATA_PATH)
    inspect_dataset(df)

    df, df_valid = prepare_analysis_data(df)

    plot_attrition_distribution(df)
    plot_department_analysis(df)
    plot_job_role_analysis(df)
    plot_age_analysis(df, df_valid)
    plot_income_analysis(df, df_valid)
    plot_tenure_analysis(df, df_valid)
    plot_categorical_analysis(df)
    print_crosstab_summaries(df)
    plot_correlation_heatmap(df)
    print_final_summary(df)

    print("\nEDA completed.")
    print("Charts saved to:", IMAGE_PATH)

def save_figure(file_name):
    IMAGE_PATH.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(IMAGE_PATH / file_name, dpi=300, bbox_inches="tight")
    plt.show()
    plt.close()

if __name__ == "__main__":
    main()