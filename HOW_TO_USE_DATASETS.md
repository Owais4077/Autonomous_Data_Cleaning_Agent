# Using Different Datasets with the AutoETL Pipeline

## Quick Start

### Option 1: Use the default dataset
```bash
python run_pipeline.py
```
This will clean `data/raw/messy_dataset.csv` and save to `data/cleaned/cleaned_dataset.csv`.

### Option 2: Specify a custom input dataset
```bash
python run_pipeline.py --input path/to/your/dataset.csv
```
Example:
```bash
python run_pipeline.py --input data/raw/my_data.csv
```

### Option 3: Specify both input and output paths
```bash
python run_pipeline.py --input data/raw/my_data.csv --output data/cleaned/my_output.csv
```

## Dataset Requirements

Your dataset should be a **CSV file** with the following structure (or similar):
- **Name**: Person's name
- **Age**: Numeric age (missing values will be filled with median)
- **Salary**: Numeric salary (missing values filled with city mean or overall mean)
- **City**: City name (will be title-cased: "new york" → "New York")
- **Joining_Date**: Date in any recognizable format (will be converted to YYYY-MM-DD)

### Example input CSV:
```csv
Name,Age,Salary,City,Joining_Date
John Doe,28,50000,New York,2021-03-15
Jane Smith,34,,San Francisco,2019-07-22
,38,76000,Los Angeles,
Peter Jones,45,95000,chicago,2018-01-05
```

## What the Pipeline Does

1. **Loads** your raw CSV file
2. **Analyzes** initial missing values and duplicates
3. **Cleans** the data by:
   - Filling missing Age with the median age
   - Filling missing Salary with the mean salary per city (or overall mean if city data unavailable)
   - Standardizing City names (title-case)
   - Formatting all Joining_Date values to YYYY-MM-DD
   - Removing duplicate rows
4. **Saves** the cleaned dataset to CSV
5. **Generates** cleaning summary reports (text and visual)

## Output Files

After running the pipeline, you'll get:
- **Cleaned CSV**: Your specified output path (default: `data/cleaned/cleaned_dataset.csv`)
- **Text Report**: `reports/cleaning_summary.txt` - Summary of changes made
- **Visual Report**: `reports/visual_summary.png` - Before/after missing value chart

## Using from Python Code

If you want to use the pipeline programmatically:

```python
from run_pipeline import run_autoetl_custom

# Run pipeline on a custom dataset
success = run_autoetl_custom(
    input_path="data/raw/my_dataset.csv",
    output_path="data/cleaned/my_cleaned_dataset.csv"
)

if success:
    print("Pipeline completed successfully!")
```

## Command-Line Examples

### Clean a specific dataset
```bash
python run_pipeline.py --input data/raw/employees.csv --output data/cleaned/employees_clean.csv
```

### Clean multiple datasets (run in sequence)
```bash
python run_pipeline.py --input data/raw/dataset1.csv --output data/cleaned/dataset1_clean.csv
python run_pipeline.py --input data/raw/dataset2.csv --output data/cleaned/dataset2_clean.csv
python run_pipeline.py --input data/raw/dataset3.csv --output data/cleaned/dataset3_clean.csv
```

### Using with PowerShell (on Windows)
```powershell
$env:PYTHONPATH='g:\pg\Autonomous_Data_Cleaning_Agent'
G:/pg/Autonomous_Data_Cleaning_Agent/.venv/Scripts/python.exe run_pipeline.py --input data/raw/my_data.csv
```

## Troubleshooting

### "File not found" error
- Make sure your input CSV path is correct (relative to the repo root)
- Check that the file exists: `ls data/raw/your_file.csv`

### "Column not found" error
- The pipeline expects standard column names (Name, Age, Salary, City, Joining_Date)
- If your CSV has different column names, the cleaner will skip those columns
- You can modify `src/ai_cleaner_local.py` to handle custom column names

### Missing values not filled
- The pipeline only fills missing numeric values (Age, Salary)
- Missing text values (Name, City) are kept as-is or filled with defaults
- Rows with missing Name are dropped during duplicate removal

## Advanced: Using with OpenAI GPT-4 (Optional)

If you want AI-powered cleaning instead of deterministic rules:

1. Install required packages:
   ```bash
   pip install pandasai==2.3.2 openai==1.0+
   ```

2. Create a `.env` file in the repo root:
   ```
   OPENAI_API_KEY="your_openai_api_key_here"
   ```

3. Run the pipeline as usual - it will automatically use AI-powered cleaning

The pipeline will fall back to the deterministic cleaner if OpenAI is not available or configured.
