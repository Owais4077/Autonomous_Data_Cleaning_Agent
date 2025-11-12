import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Tuple, Dict, List


def perform_eda(df: pd.DataFrame, dataset_name: str = "Dataset") -> Dict:
    """
    Perform automatic Exploratory Data Analysis on any dataset.
    
    Returns:
        Dictionary with EDA statistics and insights
    """
    print(f"\n{'='*60}")
    print(f"EXPLORATORY DATA ANALYSIS: {dataset_name}")
    print(f"{'='*60}")
    
    eda_report = {}
    
    # Basic Info
    print(f"\n📊 BASIC INFORMATION:")
    print(f"  Shape: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  Column Names: {list(df.columns)}")
    print(f"  Data Types:\n{df.dtypes.to_string()}")
    
    eda_report['shape'] = df.shape
    eda_report['columns'] = list(df.columns)
    eda_report['dtypes'] = df.dtypes.to_dict()
    
    # Missing Values
    print(f"\n❌ MISSING VALUES:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'Count': missing, 'Percentage': missing_pct})
    print(missing_df[missing_df['Count'] > 0].to_string() if missing.sum() > 0 else "  No missing values!")
    
    eda_report['missing_values'] = missing.to_dict()
    
    # Duplicates
    duplicates = df.duplicated().sum()
    print(f"\n🔄 DUPLICATES:")
    print(f"  Total duplicate rows: {duplicates}")
    if duplicates > 0:
        print(f"  Percentage: {(duplicates/len(df)*100):.2f}%")
    
    eda_report['duplicates'] = duplicates
    
    # Numeric Columns Summary
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_cols:
        print(f"\n🔢 NUMERIC COLUMNS SUMMARY:")
        print(df[numeric_cols].describe().to_string())
        eda_report['numeric_summary'] = df[numeric_cols].describe().to_dict()
    
    # Categorical Columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    if categorical_cols:
        print(f"\n📝 CATEGORICAL COLUMNS:")
        for col in categorical_cols:
            unique_count = df[col].nunique()
            print(f"  {col}: {unique_count} unique values")
            if unique_count <= 10:
                print(f"    Values: {df[col].value_counts().to_dict()}")
        eda_report['categorical_cols'] = categorical_cols
    
    # Data Quality Score
    quality_score = (1 - (missing.sum() / (len(df) * len(df.columns)))) * 100
    quality_score -= (duplicates / len(df)) * 10  # Deduct for duplicates
    quality_score = max(0, quality_score)
    
    print(f"\n📈 DATA QUALITY SCORE: {quality_score:.2f}%")
    eda_report['quality_score'] = quality_score
    
    return eda_report


def detect_column_types(df: pd.DataFrame) -> Dict[str, List[str]]:
    """
    Auto-detect column types and purposes (numeric, date, categorical, text).
    """
    column_mapping = {
        'numeric': [],
        'datetime': [],
        'categorical': [],
        'text': []
    }
    
    for col in df.columns:
        # Try numeric
        if pd.api.types.is_numeric_dtype(df[col]):
            column_mapping['numeric'].append(col)
        # Try datetime
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            column_mapping['datetime'].append(col)
        else:
            # Try to parse as datetime
            try:
                pd.to_datetime(df[col], errors='coerce')
                if df[col].apply(lambda x: isinstance(x, str) and len(x) < 50).all():
                    column_mapping['datetime'].append(col)
                else:
                    column_mapping['text'].append(col)
            except:
                # Check if categorical (few unique values)
                if df[col].nunique() < len(df) * 0.5:
                    column_mapping['categorical'].append(col)
                else:
                    column_mapping['text'].append(col)
    
    return column_mapping


def auto_clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Automatically clean any dataset based on detected column types.
    
    Actions:
    1. Remove complete duplicate rows
    2. Fill missing numeric values (median for outliers, mean otherwise)
    3. Standardize categorical text (title case, strip whitespace)
    4. Parse and standardize datetime columns
    5. Remove rows with critical missing values (>50% missing in a row)
    """
    print(f"\n{'='*60}")
    print("AUTOMATIC DATA CLEANING")
    print(f"{'='*60}")
    
    df = df.copy()
    initial_shape = df.shape
    
    # Detect column types
    col_types = detect_column_types(df)
    print(f"\nDetected column types:")
    for col_type, cols in col_types.items():
        if cols:
            print(f"  {col_type}: {cols}")
    
    # 1. Remove complete duplicates
    duplicates_before = df.duplicated().sum()
    df = df.drop_duplicates(ignore_index=True)
    duplicates_removed = duplicates_before - df.duplicated().sum()
    if duplicates_removed > 0:
        print(f"\n✅ Removed {duplicates_removed} duplicate rows")
    
    # 2. Handle numeric columns
    for col in col_types['numeric']:
        missing = df[col].isnull().sum()
        if missing > 0:
            # Use median for robustness to outliers
            fill_value = df[col].median()
            df[col] = df[col].fillna(fill_value)
            print(f"✅ Filled {missing} missing values in '{col}' with median: {fill_value:.2f}")
    
    # 3. Handle categorical columns
    for col in col_types['categorical']:
        missing = df[col].isnull().sum()
        if missing > 0:
            # Fill with mode or 'Unknown'
            mode_val = df[col].mode()
            fill_value = mode_val[0] if len(mode_val) > 0 else 'Unknown'
            df[col] = df[col].fillna(fill_value)
            print(f"✅ Filled {missing} missing values in '{col}' with mode: {fill_value}")
        
        # Standardize text (title case, strip whitespace)
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip().str.title()
    
    # 4. Handle datetime columns
    for col in col_types['datetime']:
        missing = df[col].isnull().sum()
        try:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            if missing > 0:
                # Fill with median date or drop rows
                df[col] = df[col].fillna(df[col].median())
                print(f"✅ Filled {missing} missing dates in '{col}'")
            # Format as string YYYY-MM-DD
            df[col] = df[col].dt.strftime('%Y-%m-%d')
        except:
            print(f"⚠️  Could not parse '{col}' as datetime")
    
    # 5. Handle text columns
    for col in col_types['text']:
        missing = df[col].isnull().sum()
        if missing > 0:
            df[col] = df[col].fillna('Unknown')
            print(f"✅ Filled {missing} missing values in '{col}' with 'Unknown'")
        # Clean up whitespace
        if df[col].dtype == 'object':
            df[col] = df[col].astype(str).str.strip()
    
    # Remove rows where majority of columns are missing
    row_missing_pct = df.isnull().sum(axis=1) / len(df.columns)
    rows_to_drop = row_missing_pct[row_missing_pct > 0.5].index
    if len(rows_to_drop) > 0:
        df = df.drop(rows_to_drop, ignore_index=True)
        print(f"✅ Removed {len(rows_to_drop)} rows with >50% missing values")
    
    final_shape = df.shape
    print(f"\n📊 Summary:")
    print(f"  Before: {initial_shape[0]} rows × {initial_shape[1]} columns")
    print(f"  After:  {final_shape[0]} rows × {final_shape[1]} columns")
    print(f"  Rows removed: {initial_shape[0] - final_shape[0]}")
    
    return df


def create_eda_visualizations(df_before: pd.DataFrame, df_after: pd.DataFrame, output_path: str = "reports/eda_analysis.png"):
    """
    Create comprehensive EDA visualizations comparing before and after cleaning.
    """
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    numeric_cols = df_before.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        print(f"⚠️  No numeric columns for visualization")
        return
    
    # Create a figure with subplots
    n_cols = len(numeric_cols[:4])  # Limit to 4 columns
    fig, axes = plt.subplots(2, min(2, n_cols), figsize=(12, 8))
    fig.suptitle('Data Quality: Before vs After Cleaning', fontsize=14, fontweight='bold')
    
    if n_cols == 1:
        axes = axes.reshape(-1, 1)
    
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols[:4]):
        ax = axes[idx]
        
        # Create box plot comparison
        data_before = df_before[col].dropna()
        data_after = df_after[col].dropna()
        
        bp = ax.boxplot([data_before, data_after], labels=['Before', 'After'], patch_artist=True)
        for patch, color in zip(bp['boxes'], ['lightcoral', 'lightgreen']):
            patch.set_facecolor(color)
        
        ax.set_title(f'{col}')
        ax.set_ylabel('Value')
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Visualization saved to {output_path}")
    plt.close()
