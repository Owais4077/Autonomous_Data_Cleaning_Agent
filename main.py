#!/usr/bin/env python3
"""
╔════════════════════════════════════════════════════════════════════╗
║                                                                    ║
║     🤖 INTELLIGENT DATA CLEANING & EDA AGENT 🤖                   ║
║                                                                    ║
║  Universal data cleaning system that works with ANY CSV format    ║
║  - Auto-detects column types                                      ║
║  - Performs automatic EDA                                         ║
║  - Intelligently cleans any dataset                               ║
║  - Generates reports and visualizations                           ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

USAGE:
    python main.py --input your_data.csv
    python main.py --input your_data.csv --output cleaned.csv
    python main.py --input your_data.csv --eda-only

FEATURES:
    ✅ Works with ANY CSV (no configuration needed!)
    ✅ Auto-detects numeric, categorical, text, datetime columns
    ✅ Automatic EDA with quality scores
    ✅ Fills missing values intelligently
    ✅ Standardizes text and dates
    ✅ Removes duplicates
    ✅ Generates comprehensive reports
    ✅ Creates visualizations

INSTALL:
    pip install pandas numpy matplotlib seaborn

RUN:
    python main.py --input your_dataset.csv
"""

import os
import sys
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple


class IntelligentDataCleaner:
    """Universal data cleaning engine - works with any CSV structure"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.col_types = {}
        self.eda_report = {}
        
    def log(self, msg):
        """Print verbose messages"""
        if self.verbose:
            print(msg)
    
    def load_data(self, filepath: str) -> pd.DataFrame:
        """Load CSV file"""
        self.log(f"\n📂 Loading data from: {filepath}")
        try:
            df = pd.read_csv(filepath)
            self.log(f"✅ Data loaded successfully ({df.shape[0]} rows, {df.shape[1]} columns)")
            return df
        except Exception as e:
            self.log(f"❌ Error loading file: {e}")
            return None
    
    def detect_column_types(self, df: pd.DataFrame) -> Dict[str, List[str]]:
        """Auto-detect column types and purposes"""
        self.log(f"\n🔍 Detecting column types...")
        
        col_types = {
            'numeric': [],
            'datetime': [],
            'categorical': [],
            'text': []
        }
        
        for col in df.columns:
            # Try numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                col_types['numeric'].append(col)
            # Try datetime
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                col_types['datetime'].append(col)
            else:
                # Try to parse as datetime
                try:
                    pd.to_datetime(df[col], errors='coerce')
                    if df[col].apply(lambda x: isinstance(x, str) and len(str(x)) < 50).all():
                        col_types['datetime'].append(col)
                    else:
                        col_types['text'].append(col)
                except:
                    # Check if categorical (few unique values)
                    if df[col].nunique() < len(df) * 0.5:
                        col_types['categorical'].append(col)
                    else:
                        col_types['text'].append(col)
        
        self.col_types = col_types
        self.log("✅ Column types detected:")
        for col_type, cols in col_types.items():
            if cols:
                self.log(f"   {col_type}: {cols}")
        
        return col_types
    
    def perform_eda(self, df: pd.DataFrame, name: str = "Dataset") -> Dict:
        """Perform exploratory data analysis"""
        self.log(f"\n{'='*60}")
        self.log(f"📊 EXPLORATORY DATA ANALYSIS: {name}")
        self.log(f"{'='*60}")
        
        report = {}
        
        # Basic info
        self.log(f"\n📋 SHAPE: {df.shape[0]} rows × {df.shape[1]} columns")
        report['shape'] = df.shape
        
        # Missing values
        self.log(f"\n❌ MISSING VALUES:")
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        if missing.sum() > 0:
            for col in missing[missing > 0].index:
                self.log(f"   {col}: {missing[col]} ({missing_pct[col]}%)")
        else:
            self.log("   None!")
        report['missing'] = missing.to_dict()
        
        # Duplicates
        duplicates = df.duplicated().sum()
        self.log(f"\n🔄 DUPLICATES: {duplicates} rows ({(duplicates/len(df)*100):.2f}%)")
        report['duplicates'] = duplicates
        
        # Numeric summary
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            self.log(f"\n🔢 NUMERIC COLUMNS:")
            for col in numeric_cols:
                self.log(f"   {col}: mean={df[col].mean():.2f}, min={df[col].min():.2f}, max={df[col].max():.2f}")
        
        # Data quality score
        quality_score = (1 - (missing.sum() / (len(df) * len(df.columns)))) * 100
        quality_score -= (duplicates / max(len(df), 1)) * 10
        quality_score = max(0, min(100, quality_score))
        
        self.log(f"\n📈 DATA QUALITY SCORE: {quality_score:.2f}%")
        report['quality_score'] = quality_score
        
        self.eda_report = report
        return report
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Auto-clean dataset based on detected column types"""
        self.log(f"\n{'='*60}")
        self.log(f"🧹 AUTOMATIC DATA CLEANING")
        self.log(f"{'='*60}")
        
        df = df.copy()
        initial_rows = len(df)
        
        # 1. Remove duplicates
        duplicates = df.duplicated().sum()
        df = df.drop_duplicates(ignore_index=True)
        if duplicates > 0:
            self.log(f"✅ Removed {duplicates} duplicate rows")
        
        # 2. Handle numeric columns
        for col in self.col_types['numeric']:
            missing = df[col].isnull().sum()
            if missing > 0:
                fill_val = df[col].median()
                df[col] = df[col].fillna(fill_val)
                self.log(f"✅ Filled {missing} missing in '{col}' with median: {fill_val:.2f}")
        
        # 3. Handle categorical columns
        for col in self.col_types['categorical']:
            missing = df[col].isnull().sum()
            if missing > 0:
                mode_val = df[col].mode()
                fill_val = mode_val[0] if len(mode_val) > 0 else 'Unknown'
                df[col] = df[col].fillna(fill_val)
                self.log(f"✅ Filled {missing} missing in '{col}' with: {fill_val}")
            # Standardize text
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip().str.title()
        
        # 4. Handle datetime columns
        for col in self.col_types['datetime']:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                missing = df[col].isnull().sum()
                if missing > 0:
                    df[col] = df[col].fillna(df[col].median())
                df[col] = df[col].dt.strftime('%Y-%m-%d')
                if missing > 0:
                    self.log(f"✅ Parsed and filled {missing} dates in '{col}'")
            except:
                self.log(f"⚠️  Could not parse '{col}' as datetime")
        
        # 5. Handle text columns
        for col in self.col_types['text']:
            missing = df[col].isnull().sum()
            if missing > 0:
                df[col] = df[col].fillna('Unknown')
                self.log(f"✅ Filled {missing} missing in '{col}' with 'Unknown'")
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        
        # 6. Remove rows with >50% missing
        row_missing = df.isnull().sum(axis=1) / len(df.columns)
        rows_drop = row_missing[row_missing > 0.5].index
        if len(rows_drop) > 0:
            df = df.drop(rows_drop, ignore_index=True)
            self.log(f"✅ Removed {len(rows_drop)} rows with >50% missing values")
        
        self.log(f"\n📊 SUMMARY:")
        self.log(f"   Before: {initial_rows} rows")
        self.log(f"   After:  {len(df)} rows")
        self.log(f"   Removed: {initial_rows - len(df)} rows")
        
        return df
    
    def save_results(self, df: pd.DataFrame, output_path: str) -> bool:
        """Save cleaned dataset"""
        try:
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            df.to_csv(output_path, index=False)
            self.log(f"\n💾 Cleaned dataset saved to: {output_path}")
            return True
        except Exception as e:
            self.log(f"❌ Error saving file: {e}")
            return False
    
    def create_visualizations(self, df_before: pd.DataFrame, df_after: pd.DataFrame, 
                             output_path: str = "eda_analysis.png") -> bool:
        """Create before/after visualizations"""
        try:
            numeric_cols = df_before.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_cols:
                self.log(f"⚠️  No numeric columns for visualization")
                return True
            
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            n_cols = min(2, len(numeric_cols[:4]))
            fig, axes = plt.subplots(2, n_cols, figsize=(12, 8))
            fig.suptitle('Data Quality: Before vs After Cleaning', fontsize=14, fontweight='bold')
            
            axes = axes.flatten() if isinstance(axes, np.ndarray) else [axes]
            
            for idx, col in enumerate(numeric_cols[:4]):
                if idx >= len(axes):
                    break
                ax = axes[idx]
                
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
            self.log(f"✅ Visualization saved to: {output_path}")
            plt.close()
            return True
        except Exception as e:
            self.log(f"⚠️  Could not create visualization: {e}")
            return True
    
    def generate_report(self, df_before: pd.DataFrame, df_after: pd.DataFrame, 
                       output_path: str = "cleaning_report.txt") -> bool:
        """Generate text report"""
        try:
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write("="*60 + "\n")
                f.write("DATA CLEANING REPORT\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"Original Data Shape: {df_before.shape[0]} rows × {df_before.shape[1]} columns\n")
                f.write(f"Cleaned Data Shape:  {df_after.shape[0]} rows × {df_after.shape[1]} columns\n")
                f.write(f"Rows Removed: {df_before.shape[0] - df_after.shape[0]}\n\n")
                
                f.write("Missing Values Before:\n")
                missing_before = df_before.isnull().sum()
                for col in missing_before[missing_before > 0].index:
                    f.write(f"  {col}: {missing_before[col]}\n")
                
                f.write("\nMissing Values After:\n")
                missing_after = df_after.isnull().sum()
                if missing_after.sum() == 0:
                    f.write("  None!\n")
                else:
                    for col in missing_after[missing_after > 0].index:
                        f.write(f"  {col}: {missing_after[col]}\n")
                
                f.write("\nColumn Types Detected:\n")
                for col_type, cols in self.col_types.items():
                    if cols:
                        f.write(f"  {col_type}: {', '.join(cols)}\n")
                
                f.write(f"\nData Quality Score: {self.eda_report.get('quality_score', 'N/A'):.2f}%\n")
            
            self.log(f"✅ Report saved to: {output_path}")
            return True
        except Exception as e:
            self.log(f"⚠️  Could not create report: {e}")
            return True


def main():
    parser = argparse.ArgumentParser(
        description="🤖 Intelligent Data Cleaning Agent - Works with ANY CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXAMPLES:
  python main.py --input data.csv
  python main.py --input data.csv --output cleaned.csv
  python main.py --input data.csv --eda-only
  python main.py --input data.csv --report-dir ./reports
        """
    )
    
    parser.add_argument('--input', type=str, required=True, help='Input CSV file path')
    parser.add_argument('--output', type=str, default=None, help='Output CSV file path')
    parser.add_argument('--report-dir', type=str, default='.', help='Directory for reports and visualizations')
    parser.add_argument('--eda-only', action='store_true', help='Only perform EDA, skip cleaning')
    
    args = parser.parse_args()
    
    # Initialize cleaner
    cleaner = IntelligentDataCleaner(verbose=True)
    
    # Load data
    df_original = cleaner.load_data(args.input)
    if df_original is None:
        return False
    
    # Detect column types
    cleaner.detect_column_types(df_original)
    
    # Perform EDA
    cleaner.perform_eda(df_original, os.path.basename(args.input))
    
    # Return after EDA if --eda-only
    if args.eda_only:
        cleaner.log("\n✅ EDA completed! Skipping cleaning (--eda-only flag)")
        return True
    
    # Clean data
    df_cleaned = cleaner.clean_data(df_original)
    
    # Save cleaned dataset
    output_path = args.output or f"{os.path.splitext(args.input)[0]}_cleaned.csv"
    if not cleaner.save_results(df_cleaned, output_path):
        return False
    
    # Generate visualizations and report
    report_path = os.path.join(args.report_dir, "cleaning_report.txt")
    viz_path = os.path.join(args.report_dir, "eda_analysis.png")
    
    cleaner.create_visualizations(df_original, df_cleaned, viz_path)
    cleaner.generate_report(df_original, df_cleaned, report_path)
    
    # Final summary
    cleaner.log(f"\n{'='*60}")
    cleaner.log(f"✅ CLEANING COMPLETE!")
    cleaner.log(f"{'='*60}")
    cleaner.log(f"\n📁 Output Files:")
    cleaner.log(f"   • Cleaned CSV: {output_path}")
    cleaner.log(f"   • Report: {report_path}")
    cleaner.log(f"   • Visualization: {viz_path}")
    
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
