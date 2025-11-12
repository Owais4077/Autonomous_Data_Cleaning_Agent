# ⚡ Quick Start Guide

## 30-Second Setup

1. **Open terminal in project folder:**
   ```powershell
   cd g:\pg\Autonomous_Data_Cleaning_Agent
   ```

2. **Run pipeline:**
   ```powershell
   $env:PYTHONPATH='g:\pg\Autonomous_Data_Cleaning_Agent'
   G:/pg/Autonomous_Data_Cleaning_Agent/.venv/Scripts/python.exe run_pipeline.py
   ```

3. **Check results:**
   ```
   ✅ Cleaned data → data/cleaned/cleaned_dataset.csv
   ✅ Report → reports/cleaning_summary.txt
   ✅ Charts → reports/eda_analysis.png
   ```

---

## With Your Own Dataset

### Step 1: Copy Your File
```powershell
# Copy your CSV to the project
Copy-Item "C:\path\to\your_data.csv" "data/raw/my_data.csv"
```

### Step 2: Run Pipeline
```powershell
python run_pipeline.py --input data/raw/my_data.csv
```

### Step 3: Get Results
```
✅ data/cleaned/cleaned_dataset.csv
✅ reports/cleaning_summary.txt
✅ reports/eda_analysis.png
```

---

## All Commands

| Goal | Command |
|------|---------|
| Clean default file | `python run_pipeline.py` |
| Analyze your data | `python run_pipeline.py --input data.csv --eda-only` |
| Clean your data | `python run_pipeline.py --input data.csv` |
| Custom output | `python run_pipeline.py --input in.csv --output out.csv` |
| Get help | `python run_pipeline.py --help` |

---

## What It Does

### 🔍 EDA (Exploratory Data Analysis)
- Shows data shape and structure
- Lists missing values
- Finds duplicates
- Calculates data quality score (0-100%)
- Shows numeric statistics
- Lists categorical values

### 🧹 Cleaning
- **Fills missing numeric values** → Median
- **Fills missing categories** → Mode or 'Unknown'
- **Standardizes text** → Title Case, trim spaces
- **Parses dates** → YYYY-MM-DD format
- **Removes duplicates** → Gone!
- **Removes incomplete rows** → If >50% missing

### 📊 Reports
- **Summary report** → Text file showing what was cleaned
- **Visualizations** → Charts showing before/after
- **Cleaned CSV** → Ready for analysis/ML/dashboards

---

## Examples

### Scenario 1: Employee Data
```bash
# You have: employees.csv with missing salaries, bad dates, duplicates
python run_pipeline.py --input data/raw/employees.csv

# You get: Clean employee data ready for HR analysis
```

### Scenario 2: Customer Data
```bash
# You have: customers.csv with messy phone numbers, duplicate names
python run_pipeline.py --input data/raw/customers.csv

# You get: Clean customer list ready for CRM
```

### Scenario 3: Sales Data
```bash
# You have: sales.csv with missing amounts, inconsistent regions
python run_pipeline.py --input data/raw/sales.csv

# You get: Clean sales data ready for analysis
```

---

## Features

✅ **Works with ANY CSV** - Auto-detects structure  
✅ **No configuration** - Just run it!  
✅ **Smart cleaning** - Adapts to your data  
✅ **Auto reports** - EDA + summary  
✅ **Visualizations** - See your data  
✅ **Batch ready** - Clean many files  
✅ **Python API** - Use in your code  
✅ **Optional AI** - GPT-4 cleaning (with setup)  

---

## Troubleshooting

### "File not found"
- Make sure your CSV is in `data/raw/` folder
- Use relative path: `data/raw/myfile.csv`

### "No output files"
- Check `data/cleaned/` and `reports/` folders
- Files are created automatically

### Want to see what's in your data first?
```bash
python run_pipeline.py --input data.csv --eda-only
```
This analyzes WITHOUT cleaning.

---

## Next Steps

1. **Try with default data:**
   ```bash
   python run_pipeline.py
   ```

2. **Copy your CSV to `data/raw/`**

3. **Run pipeline on your data:**
   ```bash
   python run_pipeline.py --input data/raw/your_file.csv
   ```

4. **Check the outputs:**
   - Cleaned CSV in `data/cleaned/`
   - Summary in `reports/cleaning_summary.txt`
   - Charts in `reports/eda_analysis.png`

5. **Use your clean data:**
   ```python
   import pandas as pd
   df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
   # Now ready for ML, analysis, dashboards, etc.
   ```

---

## 📞 Quick Reference

```bash
# Most common:
python run_pipeline.py --input data/raw/your_file.csv

# See what will be cleaned (no actual cleaning):
python run_pipeline.py --input data/raw/your_file.csv --eda-only

# Save to custom location:
python run_pipeline.py --input in.csv --output my_clean_data.csv

# Use AI cleaning (requires .env with API key):
python run_pipeline.py --input data.csv --use-ai

# Show all options:
python run_pipeline.py --help
```

---

## ✨ That's It!

You now have a **universal data cleaning agent** that works with ANY CSV file!

- 📁 **Any structure** - Auto-detects columns
- 🔍 **Auto EDA** - Quality scores and analysis
- 🧹 **Smart cleaning** - Adapts to your data
- 📊 **Beautiful reports** - Understand your results

**Just point it at your CSV and let it work!** 🚀
