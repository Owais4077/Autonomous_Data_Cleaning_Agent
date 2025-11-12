# 🤖 Data Cleaning Agent - Complete Usage Guide

## What This Is

A **universal data cleaning tool** that works with **ANY CSV file** - no configuration needed!

You give it messy data → It automatically cleans it and gives you clean data back.

---

## Installation (One-Time Setup)

### Step 1: Install Python Packages

```bash
pip install pandas numpy matplotlib seaborn
```

That's it! You're ready to go.

---

## How to Use

### Basic Usage (Simplest Way)

```bash
python main.py --input your_data.csv
```

**What happens:**
- ✅ Loads your CSV file
- ✅ Analyzes the data (detects column types automatically)
- ✅ Fills missing values intelligently
- ✅ Removes duplicates
- ✅ Standardizes text and dates
- ✅ Saves cleaned CSV as: `your_data_cleaned.csv`
- ✅ Generates report and visualization

---

### Advanced Options

#### 1. Specify Output File Name
```bash
python main.py --input messy.csv --output clean_data.csv
```

#### 2. Save Reports to Specific Directory
```bash
python main.py --input messy.csv --report-dir ./my_reports
```

#### 3. Only See Analysis (Don't Clean)
```bash
python main.py --input messy.csv --eda-only
```
This just shows you data quality analysis without making changes.

#### 4. Combine Options
```bash
python main.py --input messy.csv --output cleaned.csv --report-dir ./reports
```

---

## What Gets Auto-Detected

The tool **automatically identifies** what type each column is:

### 🔢 Numeric Columns
- **Action:** Fill missing with median value (robust to outliers)
- **Example:** Age, Salary, Count

### 📝 Categorical Columns  
- **Action:** Fill missing with most common value (mode)
- **Example:** City, Department, Status

### 📅 Datetime Columns
- **Action:** Parse dates, normalize to YYYY-MM-DD format
- **Example:** Birth_Date, Created_Date

### 📄 Text Columns
- **Action:** Trim whitespace, standardize capitalization
- **Example:** Name, Description, Comments

### 🧹 General Cleaning
- **Duplicates:** Removes exact duplicate rows
- **Heavy Missing:** Removes rows that are >50% empty
- **Whitespace:** Trims leading/trailing spaces

---

## Output Files

After running, you get:

```
your_data_cleaned.csv          ← Your clean data! Use this
cleaning_report.txt             ← What was cleaned (human readable)
eda_analysis.png                ← Before/After visualization
```

---

## Examples

### Example 1: Clean a Single File

**Your file:** `sales_data.csv` (messy, with missing values)

```bash
python main.py --input sales_data.csv
```

**Result:** `sales_data_cleaned.csv` (ready to use!)

---

### Example 2: Clean Multiple Files (One at a Time)

```bash
python main.py --input file1.csv --output cleaned_file1.csv
python main.py --input file2.csv --output cleaned_file2.csv
python main.py --input file3.csv --output cleaned_file3.csv
```

---

### Example 3: Just Analyze Without Cleaning

```bash
python main.py --input my_data.csv --eda-only
```

See quality score, missing values, data types - without modifying the file.

---

## What Each Output File Contains

### 📊 `your_data_cleaned.csv`
- Clean, ready-to-use CSV file
- Missing values filled
- Duplicates removed
- Text standardized
- Dates normalized

### 📄 `cleaning_report.txt`
```
============================================================
DATA CLEANING REPORT
============================================================

Original Data Shape: 1000 rows × 15 columns
Cleaned Data Shape:  950 rows × 15 columns
Rows Removed: 50

Missing Values Before:
  Age: 25
  Salary: 10
  Email: 5

Missing Values After:
  None!

Column Types Detected:
  numeric: Age, Salary, Experience
  categorical: Department, Location
  datetime: Hire_Date
  text: Name, Email
```

### 🖼️ `eda_analysis.png`
Visual comparison of data **before** and **after** cleaning with box plots.

---

## Common Questions

### Q: What if my CSV has a different date format?
**A:** The tool auto-detects and normalizes common formats (MM/DD/YYYY, DD-MM-YYYY, etc.) to YYYY-MM-DD

### Q: What if column names have spaces?
**A:** Works fine! The tool handles spaces in column names automatically.

### Q: Can I clean multiple files at once?
**A:** Yes! Run the command multiple times, once for each file.

### Q: What if a column has ALL missing values?
**A:** It will fill with 'Unknown' for text, or skip numeric if all null.

### Q: How does it know if a column is categorical vs text?
**A:** If it has fewer unique values than 50% of total rows, it's categorical.

### Q: Can I customize the cleaning rules?
**A:** The main script is in `main.py` - you can edit the cleaning logic if needed.

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'pandas'"
**Fix:** Run this:
```bash
pip install pandas numpy matplotlib seaborn
```

### Error: "File not found"
**Check:**
- Is your CSV file in the correct location?
- Use full path: `python main.py --input C:\Users\YourName\Desktop\file.csv`

### Error: "No numeric columns for visualization"
**OK:** Just means your CSV has no numbers - report still generated.

---

## Quick Start Examples

**Clean your first file:**
```bash
python main.py --input data.csv
```

**Clean with custom output:**
```bash
python main.py --input raw_data.csv --output my_cleaned_data.csv
```

**Just see the analysis:**
```bash
python main.py --input data.csv --eda-only
```

**Save everything to a reports folder:**
```bash
python main.py --input data.csv --report-dir ./reports
```

---

## Need Help?

- Check that your CSV file path is correct
- Make sure pandas/numpy are installed: `pip install pandas numpy`
- Read the cleaning_report.txt to see what was changed
- Look at eda_analysis.png to see before/after comparison

---

**That's it! Your data is now clean and ready to use.** 🎉
