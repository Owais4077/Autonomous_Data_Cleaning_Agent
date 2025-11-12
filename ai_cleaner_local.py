import pandas as pd
from datetime import datetime


def ai_clean(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deterministic fallback cleaner that mimics the cleaning steps described in the
    original AI prompt so the pipeline can run without OpenAI/pandasai.

    Actions performed:
    1. Fill missing 'Age' values with the median age.
    2. Fill missing 'Salary' values with the mean salary for the respective 'City'.
    3. Normalize capitalization in the 'City' column (title case).
    4. Ensure the 'Joining_Date' column is in 'YYYY-MM-DD' format (invalid -> NaT).
    5. Remove duplicate rows.
    6. Save cleaned CSV to 'data/cleaned/cleaned_dataset.csv'.
    """
    print("\nRunning local deterministic data cleaner...")

    # Make a working copy
    df = df.copy()

    # 1) Fill missing Age with median (numeric only)
    if 'Age' in df.columns:
        try:
            median_age = pd.to_numeric(df['Age'], errors='coerce').median()
            df['Age'] = pd.to_numeric(df['Age'], errors='coerce').fillna(median_age).astype(int)
            print(f"Filled missing Age with median: {median_age}")
        except Exception as e:
            print(f"Warning filling Age: {e}")

    # 2) Fill missing Salary using mean per City
    if 'Salary' in df.columns:
        try:
            df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')
            if 'City' in df.columns:
                # normalize city temporarily for grouping
                city_norm = df['City'].astype(str).str.title()
                salary_by_city = df.groupby(city_norm)['Salary'].transform(lambda x: x.fillna(x.mean()))
                df['Salary'] = df['Salary'].fillna(salary_by_city)
            # Finally, fill any remaining salary with overall mean
            overall_mean = df['Salary'].mean()
            df['Salary'] = df['Salary'].fillna(overall_mean)
            print(f"Filled missing Salary using city mean and overall mean: {overall_mean}")
        except Exception as e:
            print(f"Warning filling Salary: {e}")

    # 3) Normalize City capitalization
    if 'City' in df.columns:
        df['City'] = df['City'].astype(str).str.strip().replace({'nan': None}).where(~df['City'].astype(str).isin(['None', 'None']), None)
        df['City'] = df['City'].fillna('').apply(lambda x: x.title() if x != '' else x)

    # 4) Normalize Joining_Date to YYYY-MM-DD
    if 'Joining_Date' in df.columns:
        df['Joining_Date'] = pd.to_datetime(df['Joining_Date'], errors='coerce')
        # Format dates; keep NaT as empty string or NaN
        df['Joining_Date'] = df['Joining_Date'].dt.strftime('%Y-%m-%d')
        # pd.to_datetime + strftime turns NaT into NaN; replace 'NaT' or NaN with empty string
        df['Joining_Date'] = df['Joining_Date'].fillna('')

    # 5) Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates(ignore_index=True)
    after = len(df)
    print(f"Removed duplicates: {before - after}")

    # Ensure output folder exists
    import os
    os.makedirs('data/cleaned', exist_ok=True)

    # Save cleaned CSV
    output_path = 'data/cleaned/cleaned_dataset.csv'
    try:
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned dataset to {output_path}")
    except Exception as e:
        print(f"Warning saving cleaned dataset: {e}")

    return df
