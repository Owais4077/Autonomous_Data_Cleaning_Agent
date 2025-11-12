# ⚡ QUICK START - 30 Second Guide

## Installation (Do Once)
```bash
pip install pandas numpy matplotlib seaborn
```

## Clean Your Data (Do Every Time)
```bash
python main.py --input your_file.csv
```

## Done! 🎉
Your cleaned file is ready:
- `your_file_cleaned.csv` ← **Use this!**
- `cleaning_report.txt` - See what was changed
- `eda_analysis.png` - Before/after comparison

---

## More Options

| What You Want | Command |
|---|---|
| **Basic cleaning** | `python main.py --input data.csv` |
| **Custom output name** | `python main.py --input data.csv --output clean.csv` |
| **Save reports elsewhere** | `python main.py --input data.csv --report-dir ./reports` |
| **Just analyze (no clean)** | `python main.py --input data.csv --eda-only` |
| **See all options** | `python main.py --help` |

---

## What It Does Automatically

✅ **Numeric columns** (Age, Salary)
  - Fills missing with median value
  
✅ **Categorical columns** (City, Department)  
  - Fills missing with most common value
  
✅ **Dates** (Birth_Date, Join_Date)
  - Parses different formats, normalizes to YYYY-MM-DD
  
✅ **Text** (Name, Description)
  - Trims spaces, fixes capitalization
  
✅ **Overall**
  - Removes duplicates
  - Removes mostly-empty rows
  - Generates quality report

---

## File Structure

```
project/
├── main.py              ← The cleaner
├── YOUR_FILE.csv        ← Put your data here
└── YOUR_FILE_cleaned.csv ← Get your clean data here
```

---

## Examples

```bash
# Clean a customer file
python main.py --input customers.csv

# Clean and save with new name
python main.py --input messy.csv --output clean.csv

# Clean multiple files
python main.py --input file1.csv
python main.py --input file2.csv

# Just analyze (don't change data)
python main.py --input data.csv --eda-only
```

---

## Output Files

| File | Purpose |
|---|---|
| `data_cleaned.csv` | ⭐ Your clean data - ready to use! |
| `cleaning_report.txt` | What was cleaned & why |
| `eda_analysis.png` | Before/after visualization |

---

## Done! 🚀

Your data is clean and ready. Use it in Excel, Python, Power BI, SQL, or any tool!

---

**Want more details?** Read `USAGE_GUIDE.md`

**Have code questions?** See `examples.py`

**Want to understand everything?** Read `README_MAIN.md`
