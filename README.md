# HR Analytics — Employee Attrition & Performance

**An end-to-end data analytics and business intelligence project using Python, Pandas, Matplotlib, and Power BI to explore employee attrition patterns.**

---

## 📌 Project Overview

Employee attrition can affect workforce stability, recruitment costs, team productivity, and workforce planning.

This project analyzes an HR dataset through data understanding, data cleaning, exploratory data analysis (EDA), and Power BI dashboard development. It transforms employee data into visual insights that help HR teams explore attrition patterns and identify areas for further investigation.

## ❗ Problem Statement

Employee attrition can increase recruitment and training costs, disrupt team productivity, and affect organizational stability. HR teams need to understand how attrition varies across departments, job roles, and other employee attributes to identify where further investigation may be useful.

This project addresses that need by cleaning and exploring HR data with Python and Pandas, then presenting selected workforce metrics and attrition comparisons in an interactive Power BI dashboard.

**Goal:** Provide an accessible, data-driven view of employee attrition patterns to support further HR analysis and workforce planning.

## 🎯 Project Objectives

- Inspect the structure and quality of the HR dataset.
- Identify duplicate records, missing attrition labels, and suspicious income values.
- Prepare a processed dataset for analysis.
- Explore attrition patterns across available employee attributes.
- Build an interactive Power BI dashboard with KPI cards, charts, and slicers.
- Communicate findings and data limitations transparently.

## 📊 Dashboard Preview

![HR Analytics Dashboard](images/hr_analytics_dashboard.png)

*The interactive Power BI dashboard presents key workforce metrics, employee attrition rates, and comparisons across departments, job roles, gender, and overtime status through charts and interactive filters.*

### Dashboard Features

| Feature | Description |
|---|---|
| Total Employees | Displays the total distinct employee count. |
| Employees Left | Displays employees labelled as having left. |
| Attrition Rate | Shows the attrition rate calculated by the dashboard measure. |
| Employees Stayed | Displays employees labelled as having stayed. |
| Average Monthly Income | Shows the average monthly income metric. |
| Department Slicer | Filters the dashboard by department. |
| Job Role Slicer | Filters the dashboard by job role. |
| Gender Slicer | Filters the dashboard by gender category. |
| Attrition Charts | Compares attrition rates by department, job role, gender, and overtime status. |

## 📈 Key Dashboard Metrics

The following values were visible in the dashboard's default view.

| KPI | Value |
|---|---:|
| Total Employees | 1,500 |
| Employees Left | 282 |
| Employees Stayed | 1,189 |
| Attrition Rate | 19.17% |
| Average Monthly Income | ₹26,877 |

**Data interpretation note:** Employees Left and Employees Stayed total 1,471, which is 29 fewer than the total of 1,500. Missing or unclassified attrition labels mean these categories do not account for every record. Interpret the attrition rate according to the dashboard measure's denominator.

## 🧰 Tools & Technologies

| Technology | Purpose |
|---|---|
| Python | Data inspection and analysis |
| Pandas | Data manipulation and cleaning |
| Matplotlib | Exploratory data visualization |
| Jupyter Notebook | Interactive analysis and documentation |
| Power BI | Interactive dashboards and reporting |
| DAX | Measures and calculations |
| Git & GitHub | Version control and project sharing |

## 🔄 Project Workflow

1. **Data Understanding:** Inspected the dataset structure, columns, and data types.
2. **Data Cleaning:** Identified duplicate records, missing values, and suspicious values.
3. **Exploratory Data Analysis:** Explored distributions and relationships using Python and visualizations.
4. **Dashboard Development:** Built Power BI KPI cards, charts, measures, and interactive slicers.
5. **Interpretation:** Presented descriptive patterns while documenting data-quality limitations.

## 🧩 Challenges Faced & Solutions

During this project, I encountered several data-quality and reporting challenges. I investigated these issues using Python, Pandas, and Power BI and documented the limitations that still require validation.

### 1. Handling Duplicate Records

**Challenge:** The raw dataset contained duplicate records that could affect employee counts and distort the analysis.

**Solution:** Used Python and Pandas to identify and remove 30 duplicate records, reducing the dataset from 1,530 rows to 1,500 rows.

**Outcome:** Prepared a dataset with fewer duplicate records for further analysis.

### 2. Dealing with Missing Attrition Labels

**Challenge:** Some employee records did not contain an Attrition label, making it difficult to classify every employee as having left or stayed.

**Solution:** Identified 22 missing Attrition labels during data cleaning and documented the issue instead of assigning unverified employee outcomes.

**Outcome:** Improved transparency and avoided treating missing information as a confirmed attrition status.

### 3. Identifying Suspicious Income Values

**Challenge:** Six records contained a `MonthlyIncome` value of `999999`, which appeared unusual compared with typical income values in the dataset.

**Solution:** Flagged these values for validation and examined income distributions with and without the flagged records. The dashboard's average monthly income measure excludes values equal to or above `999999`.

**Outcome:** Reduced the influence of the flagged values on the income metric while documenting the need to validate them against the original data source.

### 4. Investigating Differences in Employee Counts

**Challenge:** The dashboard displayed 1,500 total employees, but the Employees Left and Employees Stayed categories added up to only 1,471.

**Solution:** Compared the displayed metrics and documented the discrepancy. Missing or unclassified Attrition labels are a relevant data-quality concern, but the exact reason for all 29 unaccounted records still requires validation.

**Outcome:** Highlighted the importance of checking missing values, category totals, and metric definitions before drawing conclusions.

### 5. Developing an Interactive Dashboard

**Challenge:** Static charts alone would not allow users to explore attrition patterns across different employee categories.

**Solution:** Built a Power BI dashboard with KPI cards, attrition charts, and interactive slicers for Department, Job Role, and Gender. The charts compare attrition patterns by department, job role, gender, and overtime status.

**Outcome:** Created an interactive dashboard that allows users to explore workforce metrics from different perspectives.

### 6. Communicating Data Limitations

**Challenge:** Missing labels, suspicious income values, and differences in category totals could affect the interpretation of the results.

**Solution:** Documented these issues in the project report and README instead of presenting the dashboard metrics as completely validated results.

**Outcome:** Made the analysis more transparent and identified areas that require further investigation before business decisions are made.

## 🗂️ Project Structure

```text
HR-Analytics/
├── data/
│   ├── raw/
│   │   └── hr_analytics_raw.csv
│   └── processed/
│       └── hr_analytics_clean.csv
├── images/
│   ├── hr_analytics_dashboard.png
│   └── [EDA visualization images]
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_exploratory_data_analysis.ipynb
├── power_bi/
│   └── hr_analytics.png.pbix
├── src/
│   ├── data_understanding.py
│   ├── data_cleaning.py
│   └── exploratory_data_analysis.py
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/anjanatanguturi2407-maker/HR-Analytics.git
cd HR-Analytics
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

### 3. Install the Required Libraries

```bash
pip install pandas matplotlib jupyter
```

Install any additional libraries required by your notebooks or scripts.

### 4. Run the Notebooks

Open Jupyter Notebook or JupyterLab and run the notebooks in this order:

1. `notebooks/01_data_understanding.ipynb`
2. `notebooks/02_data_cleaning.ipynb`
3. `notebooks/03_exploratory_data_analysis.ipynb`

### 5. Open the Power BI Dashboard

Open the `.pbix` report from the `power_bi/` folder in Power BI Desktop. If prompted, select `data/processed/hr_analytics_clean.csv` as the data source and verify that the report refreshes successfully.

## ⚠️ Data Quality & Limitations

| Finding | Details |
|---|---|
| Raw dataset | 1,530 rows |
| Duplicate records removed | 30 |
| Processed dataset | 1,500 rows |
| Missing Attrition labels | 22 identified during cleaning |
| Suspicious income values | Six `MonthlyIncome` values of `999999` flagged for validation |
| Employee category totals | Employees Left and Employees Stayed total 1,471 |

The average monthly income measure excludes suspicious high-income values identified during data inspection. These values have not been definitively validated and should be checked against the original source before drawing conclusions about income.

Additional limitations:

- Missing or unclassified values can affect metric interpretation.
- The reason for the 29-record difference between total employees and classified attrition categories requires further validation.
- The dataset may not represent every organization or workforce.
- Observed relationships do not prove that a particular attribute causes attrition.
- Dashboard metrics can change when slicers are applied.
- Confirm that the dataset is permitted to be shared publicly before uploading employee data to GitHub.

## 💼 Business Value

The dashboard allows users to explore attrition patterns across departments, job roles, gender categories, and overtime status.

These comparisons can help HR teams identify areas for further investigation, support evidence-informed workforce discussions, and improve visibility into workforce metrics.

The report is an exploratory decision-support tool. It does not establish the causes of employee attrition or prove that any particular employee attribute causes turnover.

## 🧠 Skills Demonstrated

- Data inspection and data-quality assessment
- Data cleaning using Python and Pandas
- Exploratory data analysis
- Data visualization with Matplotlib
- KPI design and DAX measures
- Power BI dashboard development
- Interactive reporting and data interpretation
- Analytical communication
- Project organization and technical documentation
- Git and GitHub version control

## 👩‍💻 Author

**Anjana Tanguturi**

Aspiring Data Analyst | Python | SQL | Power BI | Data Analytics

---

*Portfolio project focused on practical data analytics, business intelligence, data-quality assessment, and data-driven decision support.*