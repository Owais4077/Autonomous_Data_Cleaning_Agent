#!/usr/bin/env python3
"""
Intelligent ETL pipeline with automatic EDA and adaptive cleaning.

Features:
- Auto-detects dataset structure
- Performs EDA automatically
- Cleans any CSV dataset intelligently
- Generates visualizations and reports

Usage:
    python run_pipeline.py                                    # Uses default: data/raw/messy_dataset.csv
    python run_pipeline.py --input data/raw/my_dataset.csv   # Uses custom input file
    python run_pipeline.py --input data/raw/my_data.csv --output data/cleaned/my_output.csv
    python run_pipeline.py --input data/raw/my_data.csv --eda-only  # EDA only, no cleaning
"""

import os
import sys
import argparse
from src.data_loader import load_data, initial_analysis
from src.auto_eda_cleaner import perform_eda, auto_clean_dataset, create_eda_visualizations
try:
    from src.ai_cleaner import ai_clean
except Exception:
    from src.ai_cleaner_local import ai_clean
    print("Using local deterministic ai_clean (fallback, no OpenAI available).")
from src.summarizer import summarize_cleaning


def run_autoetl_custom(input_path, output_path=None, eda_only=False, use_ai=False):
    """
    Orchestrates the intelligent AutoETL pipeline for any dataset.
    
    Args:
        input_path (str): Path to the raw CSV file to analyze/clean
        output_path (str): Path where cleaned CSV will be saved 
                          (default: data/cleaned/cleaned_dataset.csv)
        eda_only (bool): If True, only perform EDA, don't clean
        use_ai (bool): If True, try to use AI-powered cleaning (requires OpenAI API key)
    """
    print(f"\n{'='*70}")
    print(f"INTELLIGENT DATA CLEANING & EDA PIPELINE")
    print(f"{'='*70}")
    print(f"Input file: {input_path}")
    
    # Validate input file exists
    if not os.path.exists(input_path):
        print(f"❌ ERROR: Input file '{input_path}' not found!")
        return False
    
    # Set default output path if not provided
    if output_path is None:
        output_path = "data/cleaned/cleaned_dataset.csv"
    
    print(f"Output file: {output_path}")
    
    # Step 1: Load raw data
    print(f"\n📂 Loading data...")
    original_df = load_data(input_path)
    
    if original_df is None:
        print("❌ ETL process halted due to data loading failure.")
        return False
    
    # Step 2: Perform EDA on original data
    print(f"\n🔍 Performing Exploratory Data Analysis...")
    eda_report = perform_eda(original_df, dataset_name=os.path.basename(input_path))
    
    if eda_only:
        print(f"\n✅ EDA completed! Skipping cleaning (--eda-only flag set)")
        return True
    
    # Step 3: Auto-clean the data
    print(f"\n🧹 Cleaning data automatically...")
    if use_ai:
        try:
            cleaned_df = auto_clean_dataset(original_df.copy())
            print("Using AI-powered cleaning mode")
        except Exception as e:
            print(f"⚠️  AI cleaning failed: {e}")
            print("Falling back to automatic adaptive cleaning...")
            cleaned_df = auto_clean_dataset(original_df.copy())
    else:
        cleaned_df = auto_clean_dataset(original_df.copy())
    
    # Step 4: Show cleaned data info
    print(f"\n✅ CLEANING COMPLETE")
    print(f"\n📊 Final Cleaned Dataset Info:")
    print(cleaned_df.info())
    print(f"\n📋 First few rows:")
    print(cleaned_df.head(10))
    
    # Step 5: Save cleaned dataset
    print(f"\n💾 Saving cleaned dataset...")
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    try:
        cleaned_df.to_csv(output_path, index=False)
        print(f"✅ Cleaned dataset saved to: {output_path}")
    except Exception as e:
        print(f"❌ Could not save to {output_path}: {e}")
        return False
    
    # Step 6: Generate visualizations and summary
    print(f"\n📊 Generating visualizations...")
    try:
        create_eda_visualizations(original_df, cleaned_df)
    except Exception as e:
        print(f"⚠️  Could not create visualizations: {e}")
    
    print(f"\n📄 Generating summary report...")
    try:
        summarize_cleaning(original_df, cleaned_df)
    except Exception as e:
        print(f"⚠️  Could not generate summary: {e}")
    
    print(f"\n{'='*70}")
    print(f"✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"{'='*70}")
    print(f"\n📁 Output Files:")
    print(f"  • Cleaned CSV: {output_path}")
    print(f"  • Summary Report: reports/cleaning_summary.txt")
    print(f"  • Visualizations: reports/eda_analysis.png")
    print(f"\n📊 EDA Summary:")
    print(f"  • Data Quality Score: {eda_report.get('quality_score', 'N/A'):.2f}%")
    print(f"  • Original Shape: {eda_report.get('shape', 'N/A')}")
    print(f"  • Duplicate Rows: {eda_report.get('duplicates', 'N/A')}")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Intelligent Data Cleaning Agent with Automatic EDA",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_pipeline.py
  python run_pipeline.py --input data/raw/employees.csv
  python run_pipeline.py --input data/raw/data.csv --output data/cleaned/output.csv
  python run_pipeline.py --input data/raw/data.csv --eda-only
  python run_pipeline.py --input data/raw/data.csv --use-ai
        """
    )
    parser.add_argument(
        "--input",
        type=str,
        default="data/raw/messy_dataset.csv",
        help="Path to input CSV file (default: data/raw/messy_dataset.csv)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save cleaned CSV (default: data/cleaned/cleaned_dataset.csv)"
    )
    parser.add_argument(
        "--eda-only",
        action="store_true",
        help="Only perform EDA analysis, skip cleaning"
    )
    parser.add_argument(
        "--use-ai",
        action="store_true",
        help="Use AI-powered cleaning (requires OpenAI API key in .env)"
    )
    
    args = parser.parse_args()
    
    success = run_autoetl_custom(args.input, args.output, eda_only=args.eda_only, use_ai=args.use_ai)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
