# 🤖 Intelligent Data Cleaning Agent

A **universal, zero-configuration data cleaning tool** that automatically handles ANY CSV file - no setup, no configuration files needed.

## ⚡ Quick Start (30 Seconds)

```bash
# 1. Install (one time)
pip install pandas numpy matplotlib seaborn

# 2. Clean your data
python main.py --input your_data.csv

# 3. Done! Check your_data_cleaned.csv
```

That's it! Your cleaned CSV is ready to use.

---

## 🎯 What This Does

### Input
```
Your messy CSV file
├── Missing values ❌
├── Duplicate rows ❌
├── Inconsistent text ❌
├── Invalid dates ❌
└── Unknown data types ❌
```

### Process
```
🔍 Auto-detect column types
📊 Perform EDA analysis
🧹 Intelligently clean data
✅ Generate reports
```

### Output
```
✨ Clean CSV file (ready to use!)
📄 Cleaning report (what changed)
🖼️ Visualization (before/after)
```

---

## 🚀 Installation

### Requirements
- Python 3.6+ (Python 3.10+ recommended)
- 50 MB disk space

### Setup
```bash
# Install required packages
pip install pandas numpy matplotlib seaborn
```

Done! No configuration files, no setup.yaml, no environment variables needed.

---

## 📖 Usage

### Most Common Usage
```bash
python main.py --input your_file.csv
```

Creates:
- `your_file_cleaned.csv` - Your clean data
- `cleaning_report.txt` - What was changed
- `eda_analysis.png` - Before/after visualization

### All Available Options

```bash
# Specify output file name
python main.py --input messy.csv --output clean.csv

# Save reports to custom directory
python main.py --input data.csv --report-dir ./reports

# Only perform analysis (don't clean)
python main.py --input data.csv --eda-only

# Combine options
python main.py --input raw.csv --output clean.csv --report-dir ./results
```

### Get Help
```bash
python main.py --help
```

---

## 🧠 Auto-Detection & Cleaning

The tool automatically identifies what each column contains and cleans appropriately:

| Column Type | Detection | Cleaning Action |
|---|---|---|
| **Numeric** | Integer or float values | Fill missing with median |
| **Categorical** | Few unique values (<50% distinct) | Fill with mode (most common) |
| **Datetime** | Recognizable date patterns | Parse & normalize to YYYY-MM-DD |
| **Text** | String data | Trim whitespace, standardize case |

### General Cleaning
- **Duplicates**: Removes exact duplicate rows
- **Heavy Missing**: Removes rows >50% empty
- **Formatting**: Trims spaces, standardizes capitalization

---

## 📤 Output Files

### 1. `your_data_cleaned.csv` ⭐
The main output - your cleaned data, ready to use in Excel, Python, SQL, Tableau, Power BI, etc.

**Example:**
```csv
Name,Age,Salary,City,Date
John,32,65000,New York,2023-01-15
Jane,28,52000,San Francisco,2023-02-20
Bob,45,78000,Chicago,2023-03-10
```

### 2. `cleaning_report.txt`
Text summary of what was cleaned.

**Example:**
```
============================================================
DATA CLEANING REPORT
============================================================

Original Shape: 1000 rows × 5 columns
Cleaned Shape: 950 rows × 5 columns

Rows Removed: 50

Missing Values Fixed:
  Age: 25 filled with median (32.5)
  Salary: 10 filled with median (65000)
  City: 5 filled with mode (New York)

Duplicates Removed: 8 rows

Column Types:
  numeric: Age, Salary
  categorical: City
  text: Name
  datetime: Date

Data Quality Score: 93.2%
```

### 3. `eda_analysis.png`
Visual comparison showing data distribution before and after cleaning.

---

## 💡 Examples

### Example 1: Clean Customer Data
```bash
python main.py --input customers.csv --output clean_customers.csv
```

### Example 2: Clean Multiple Files
```bash
python main.py --input sales_2023.csv --output clean_sales_2023.csv
python main.py --input sales_2024.csv --output clean_sales_2024.csv
```

### Example 3: Just See Data Quality
```bash
python main.py --input data.csv --eda-only
```

Shows: Missing values, data types, duplicates, quality score - without modifying the file.

### Example 4: Organize Reports
```bash
python main.py --input raw_data.csv --report-dir ./my_reports
```

Creates organized directory:
```
my_reports/
├── cleaning_report.txt
└── eda_analysis.png
```

---

## 🔧 Advanced Usage

### Using in Python Code

```python
from main import IntelligentDataCleaner

# Initialize
cleaner = IntelligentDataCleaner(verbose=True)

# Load data
df = cleaner.load_data("data.csv")

# Analyze
cleaner.detect_column_types(df)
cleaner.perform_eda(df, "My Dataset")

# Clean
df_cleaned = cleaner.clean_data(df)

# Save
cleaner.save_results(df_cleaned, "cleaned.csv")
cleaner.create_visualizations(df, df_cleaned, "viz.png")
cleaner.generate_report(df, df_cleaned, "report.txt")
```

See `examples.py` for more detailed examples.

---

## ❓ FAQ

**Q: What CSV formats work?**
A: Any CSV file - comma, semicolon, or custom delimiters (pandas auto-detects).

**Q: What if my dates are in different formats?**
A: Auto-detected! Handles MM/DD/YYYY, DD-MM-YYYY, YYYY-MM-DD, and more.

**Q: What if a column has all missing values?**
A: Fills with 'Unknown' or skips, depending on column type.

**Q: Can I use this with Excel files?**
A: Convert to CSV first, then clean. Or use `pandas.read_excel()` in Python code.

**Q: Can I add custom cleaning logic?**
A: Yes! Edit the `clean_data()` method in `main.py` or add rules after calling it.

**Q: How do I handle sensitive data?**
A: This tool doesn't send data anywhere - everything runs locally on your machine.

**Q: What's the maximum file size?**
A: Depends on your RAM. Works well with files up to 1GB.

**Q: Can I clean multiple files at once?**
A: Run the command separately for each file, or use the batch script in `examples.py`.

---

## 🆘 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'pandas'"
**Solution:**
```bash
pip install pandas numpy matplotlib seaborn
```

### Problem: "FileNotFoundError: No such file"
**Solution:**
- Check file path is correct
- Use full path: `python main.py --input C:\Users\YourName\data.csv`
- Make sure file is actually a CSV

### Problem: "No numeric columns for visualization"
**Info:** Your CSV might not have any numbers. That's OK - reports still generated.

### Problem: Script runs but produces weird output
**Solution:**
- Check CSV encoding (should be UTF-8)
- Try: `python main.py --input data.csv --report-dir ./debug`
- Review `cleaning_report.txt` for details

### Problem: Takes too long to run
**For large files (>100MB):**
- Normal - pandas needs time to process
- Large datasets may take minutes
- Check system RAM availability

---

## 📊 Supported Column Types

The tool recognizes and handles these automatically:

```
📌 NUMERIC
   integer, float, int64, float64
   Actions: Median fill, outlier-safe

📌 CATEGORICAL  
   String columns with few unique values
   Actions: Mode fill, standardize text

📌 DATETIME
   Dates in any common format
   Actions: Parse variations, normalize to YYYY-MM-DD

📌 TEXT
   Long text fields
   Actions: Trim spaces, title case

📌 BOOLEAN
   Yes/No, True/False, 1/0
   Actions: Standardize to True/False
```

---

## 🎓 Learning Resources

- **Quick Start**: See top of this file
- **Detailed Guide**: Read `USAGE_GUIDE.md`
- **Code Examples**: Run `python examples.py 1`
- **Main Script**: `main.py` (500 lines, well-commented)

---

## 📋 File Structure

```
project/
├── main.py                      ← Main cleaning tool
├── examples.py                  ← Code examples
├── USAGE_GUIDE.md               ← Detailed usage guide
├── README.md                    ← This file
│
├── data/
│   ├── raw/                     ← Put your CSV files here
│   │   └── your_data.csv
│   └── cleaned/                 ← Output goes here
│       └── your_data_cleaned.csv
│
└── reports/                     ← Analysis outputs
    ├── cleaning_report.txt
    └── eda_analysis.png
```

---

## ✨ Key Features

✅ **Zero Configuration** - No setup files, just run it
✅ **Auto-Detection** - Understands any CSV structure
✅ **Intelligent Cleaning** - Context-aware data repair
✅ **Comprehensive Reports** - See what was cleaned
✅ **Visualizations** - Before/after comparisons
✅ **Batch Processing** - Clean multiple files
✅ **Extensible** - Easy to add custom rules
✅ **Production Ready** - Robust error handling
✅ **Fast** - Optimized pandas operations
✅ **Safe** - Never deletes original data

---

## 🎯 Common Workflows

### Workflow 1: Clean and Export
```bash
python main.py --input messy.csv --output clean.csv
# Use clean.csv in your analysis/BI tool
```

### Workflow 2: Clean Multiple Files
```bash
for file in *.csv; do
  python main.py --input "$file"
done
```

### Workflow 3: Analyze Before Deciding
```bash
python main.py --input data.csv --eda-only
# Review report, then decide if you want to clean
```

### Workflow 4: Integration
```python
# In your Python script
from main import IntelligentDataCleaner

cleaner = IntelligentDataCleaner()
df = cleaner.load_data("raw.csv")
cleaner.detect_column_types(df)
df_clean = cleaner.clean_data(df)
# Now use df_clean in your analysis
```

---

## 📝 License

Free to use for any purpose.

---

## 💬 Questions?

1. Read `USAGE_GUIDE.md` for detailed instructions
2. Check `cleaning_report.txt` to see what was cleaned
3. Review `examples.py` for code samples
4. Look at generated `eda_analysis.png` for visualizations

---

## 🎉 You're Ready!

```bash
# Try it now:
python main.py --input data.csv

# Your cleaned data will be ready in seconds!
```

Happy data cleaning! 🚀
