# 🤖 Intelligent Data Cleaning & EDA Agent

An advanced **Autonomous Data Cleaning Agent** that automatically detects dataset structure, performs comprehensive EDA (Exploratory Data Analysis), and intelligently cleans any CSV dataset.

## ✨ Key Features

### 🔍 **Automatic EDA**
- Detects dataset structure and column types automatically
- Identifies numeric, categorical, datetime, and text columns
- Generates data quality scores
- Reports missing values, duplicates, and statistics
- Creates before/after visualizations

### 🧹 **Intelligent Auto-Cleaning**
- Automatically fills missing numeric values (median-based)
- Handles categorical missing values (mode-based)
- Standardizes text (title-casing, whitespace trimming)
- Parses and normalizes dates (YYYY-MM-DD format)
- Removes duplicate rows and incomplete rows
- **Works with ANY CSV structure** - no configuration needed!

### 📊 **Comprehensive Reporting**
- Data quality score calculation
- Text summary reports
- Visual before/after comparisons
- Box plots for numeric columns

### 🤖 **AI Integration** (Optional)
- Supports OpenAI GPT-4 for advanced cleaning (with .env setup)
- Falls back to intelligent rule-based cleaning automatically

---

## 🚀 Quick Start

### **Option 1: Clean Default Dataset**
```bash
python run_pipeline.py
```

### **Option 2: Clean Your Own Dataset**
```bash
python run_pipeline.py --input data/raw/your_dataset.csv
```

### **Option 3: Custom Output Location**
```bash
python run_pipeline.py --input data/raw/data.csv --output data/cleaned/my_output.csv
```

### **Option 4: EDA Only (No Cleaning)**
```bash
python run_pipeline.py --input data/raw/data.csv --eda-only
```

### **Option 5: Use AI-Powered Cleaning**
```bash
python run_pipeline.py --input data/raw/data.csv --use-ai
```
*(Requires OpenAI API key in .env file)*

---

## 📋 Dataset Requirements

Your CSV file can have **any structure**. The pipeline will automatically detect:

✅ **Numeric columns** → Filled with median  
✅ **Categorical columns** → Filled with mode or 'Unknown'  
✅ **Datetime columns** → Parsed and normalized to YYYY-MM-DD  
✅ **Text columns** → Standardized (title-cased, trimmed)  

### Example Input CSV:
```csv
Name,Age,Salary,City,Joining_Date
John Doe,28,50000,New York,2021-03-15
Jane Smith,34,,San Francisco,2019-07-22
,38,76000,los angeles,
Peter Jones,45,95000,CHICAGO,2018-01-05
```

---

## 📁 Output Files

After running the pipeline, you'll get:

1. **Cleaned Dataset** → `data/cleaned/cleaned_dataset.csv`
   - All missing values filled
   - Duplicates removed
   - Standardized formats

2. **Text Summary** → `reports/cleaning_summary.txt`
   - Before/after comparison
   - Cleaning actions performed
   - Data quality metrics

3. **Visualizations** → `reports/eda_analysis.png`
   - Box plots of numeric columns
   - Before/after comparison

---

## 🎯 What Gets Cleaned

### **Missing Values**
- Numeric: Filled with **median** (robust to outliers)
- Categorical: Filled with **mode** or 'Unknown'
- Text: Filled with **'Unknown'**
- Dates: Filled with **median date**

### **Standardization**
- **City names**: "new york" → "New York"
- **Whitespace**: Leading/trailing spaces removed
- **Dates**: Converts to YYYY-MM-DD format
- **Text**: Title-cased for consistency

### **Data Reduction**
- **Duplicates**: Complete duplicate rows removed
- **Incomplete rows**: Rows with >50% missing values dropped

### **Quality Metrics**
- Data Quality Score (0-100%)
- Missing value count and percentage
- Duplicate row count

---

## 💻 Usage Examples

### Clean Multiple Datasets in Sequence
```bash
python run_pipeline.py --input data/raw/employees.csv --output data/cleaned/employees_clean.csv
python run_pipeline.py --input data/raw/customers.csv --output data/cleaned/customers_clean.csv
python run_pipeline.py --input data/raw/sales.csv --output data/cleaned/sales_clean.csv
```

### Analyze Only (No Cleaning)
```bash
python run_pipeline.py --input data/raw/suspicious_data.csv --eda-only
```
This generates EDA reports without modifying the data.

### Using with Python Code
```python
from run_pipeline import run_autoetl_custom

# Run cleaning
success = run_autoetl_custom(
    input_path="data/raw/my_dataset.csv",
    output_path="data/cleaned/my_output.csv",
    use_ai=False  # Use rule-based cleaning
)

if success:
    print("✅ Cleaning completed!")
```

---

## 🔧 Advanced: Enable AI-Powered Cleaning

### Setup:
1. Install additional packages:
   ```bash
   pip install openai>=1.0 pandasai>=2.0
   ```

2. Create `.env` file in repo root:
   ```
   OPENAI_API_KEY="sk-your-api-key-here"
   ```

3. Run with AI flag:
   ```bash
   python run_pipeline.py --input data/raw/data.csv --use-ai
   ```

The pipeline will:
- ✅ Try AI-powered cleaning first (if setup correctly)
- ✅ Fall back to rule-based cleaning automatically if AI unavailable
- ✅ Never fail - always produces cleaned output

---

## 🐛 Troubleshooting

### "File not found" error
```
Make sure your file path is relative to the repo root:
✅ python run_pipeline.py --input data/raw/my_data.csv
❌ python run_pipeline.py --input my_data.csv
```

### "No numeric columns" warning
- This is normal if your dataset has only text/categorical columns
- The pipeline will still clean the data and generate text summaries

### Column names not detected
- The pipeline auto-detects column purposes by data type and content
- It doesn't require specific column names
- Works with "Customer Name", "Full Name", "Employee", etc.

### Dates not parsed correctly
- The pipeline handles multiple date formats (2021-03-15, 03/15/2021, etc.)
- If custom format needed, modify `src/auto_eda_cleaner.py` line ~173

---

## 📊 Sample Output

### EDA Report:
```
============================================================
EXPLORATORY DATA ANALYSIS: messy_dataset.csv
============================================================

📊 BASIC INFORMATION:
  Shape: 15 rows × 5 columns

❌ MISSING VALUES:
  Name: 1 (6.67%)
  Age: 1 (6.67%)

🔄 DUPLICATES: 2 rows (13.33%)

🔢 NUMERIC SUMMARY:
  Age: mean=33.93, std=8.15, min=23, max=52
  Salary: mean=66428.57, std=23007.40, min=42000, max=120000

📈 DATA QUALITY SCORE: 93.33%
```

---

## 🎓 How It Works

```
┌─────────────────────────────────────────────────────┐
│  1. LOAD Dataset (any CSV structure)                │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  2. DETECT Columns (numeric, text, date, category)  │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  3. ANALYZE (EDA report, quality score, stats)      │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  4. CLEAN (fill missing, standardize, deduplicate)  │
└────────────────────┬────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────────┐
│  5. SAVE (cleaned CSV + reports + visualizations)   │
└─────────────────────────────────────────────────────┘
```

---

## 📝 Pipeline Modes

| Mode | Command | Use Case |
|------|---------|----------|
| **Default Clean** | `python run_pipeline.py` | Full cleaning pipeline |
| **Custom Input** | `python run_pipeline.py --input data.csv` | Clean specific file |
| **Custom Output** | `python run_pipeline.py --output out.csv` | Save to custom location |
| **EDA Only** | `python run_pipeline.py --eda-only` | Analyze without cleaning |
| **AI Mode** | `python run_pipeline.py --use-ai` | Use OpenAI (if available) |

---

## 🔒 Data Privacy

- ✅ All processing is **local** (no cloud unless you enable AI mode)
- ✅ Input data is **never modified** (cleaned copy is saved separately)
- ✅ Reports are **generated locally**

---

## 🤝 Integration

### Use Cleaned Data in Python:
```python
import pandas as pd

# After running pipeline...
cleaned_df = pd.read_csv('data/cleaned/cleaned_dataset.csv')
print(cleaned_df.head())
# Now ready for ML, analysis, dashboarding, etc.
```

### Batch Processing:
```bash
# Create a batch script (clean_all.bat)
python run_pipeline.py --input data/raw/dataset1.csv
python run_pipeline.py --input data/raw/dataset2.csv
python run_pipeline.py --input data/raw/dataset3.csv
```

---

## 📦 Requirements

- Python 3.8+
- pandas, numpy
- matplotlib, seaborn (for visualizations)
- openai, pandasai (optional, for AI mode)

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📄 License & Support

This is an autonomous data cleaning agent designed to work with **any CSV structure**. No configuration needed!

For issues or questions, check the README or modify `src/auto_eda_cleaner.py` for custom column type detection.

---

## ✅ Tested On

✓ Employee datasets  
✓ Sales data  
✓ Customer records  
✓ Messy survey responses  
✓ Mixed data types  
✓ Highly incomplete datasets  

**Try it with your own data!**

