#!/usr/bin/env python3
"""
Example: How to use the Data Cleaning Agent

This file shows different ways to use the cleaner in your code.
"""

from main import IntelligentDataCleaner
import os

# ============================================================================
# EXAMPLE 1: Simple One-File Cleaning
# ============================================================================
def example_simple_cleaning():
    """Simplest way - clean one file"""
    cleaner = IntelligentDataCleaner(verbose=True)
    
    # Load your messy data
    df = cleaner.load_data("data.csv")
    if df is None:
        return
    
    # Detect column types
    cleaner.detect_column_types(df)
    
    # Perform analysis
    cleaner.perform_eda(df, "My Dataset")
    
    # Clean the data
    df_cleaned = cleaner.clean_data(df)
    
    # Save results
    cleaner.save_results(df_cleaned, "cleaned_data.csv")
    cleaner.create_visualizations(df, df_cleaned, "analysis.png")
    cleaner.generate_report(df, df_cleaned, "report.txt")


# ============================================================================
# EXAMPLE 2: Batch Clean Multiple Files
# ============================================================================
def example_batch_cleaning():
    """Clean multiple files at once"""
    files = [
        "data1.csv",
        "data2.csv",
        "data3.csv"
    ]
    
    for input_file in files:
        if not os.path.exists(input_file):
            print(f"⚠️  Skipping {input_file} (not found)")
            continue
        
        print(f"\n{'='*60}")
        print(f"Processing: {input_file}")
        print(f"{'='*60}")
        
        cleaner = IntelligentDataCleaner(verbose=True)
        
        # Load, analyze, clean
        df = cleaner.load_data(input_file)
        if df is None:
            continue
        
        cleaner.detect_column_types(df)
        cleaner.perform_eda(df, input_file)
        df_cleaned = cleaner.clean_data(df)
        
        # Generate outputs with file-specific names
        base_name = os.path.splitext(input_file)[0]
        cleaner.save_results(df_cleaned, f"{base_name}_cleaned.csv")
        cleaner.create_visualizations(df, df_cleaned, f"{base_name}_analysis.png")
        cleaner.generate_report(df, df_cleaned, f"{base_name}_report.txt")


# ============================================================================
# EXAMPLE 3: Only Perform EDA (No Cleaning)
# ============================================================================
def example_eda_only():
    """Just analyze data, don't change it"""
    cleaner = IntelligentDataCleaner(verbose=True)
    
    df = cleaner.load_data("data.csv")
    if df is None:
        return
    
    cleaner.detect_column_types(df)
    eda_results = cleaner.perform_eda(df, "Data Analysis")
    
    print("\n✅ Analysis completed!")
    print(f"Data Quality Score: {eda_results['quality_score']:.2f}%")
    # Dataset NOT modified


# ============================================================================
# EXAMPLE 4: Custom Cleaning Rules
# ============================================================================
def example_custom_cleaning():
    """Extend the cleaner with custom rules"""
    
    cleaner = IntelligentDataCleaner(verbose=True)
    
    df = cleaner.load_data("data.csv")
    if df is None:
        return
    
    cleaner.detect_column_types(df)
    cleaner.perform_eda(df, "Data Analysis")
    
    # Apply standard cleaning
    df_cleaned = cleaner.clean_data(df)
    
    # Add YOUR custom cleaning rules on top
    # Example: Remove rows where Age < 18
    initial = len(df_cleaned)
    df_cleaned = df_cleaned[df_cleaned['Age'] >= 18]
    removed = initial - len(df_cleaned)
    if removed > 0:
        print(f"✅ Removed {removed} rows with Age < 18")
    
    # Example: Convert salary to thousands
    if 'Salary' in df_cleaned.columns:
        df_cleaned['Salary'] = df_cleaned['Salary'] / 1000
        print(f"✅ Converted Salary to thousands")
    
    # Save results
    cleaner.save_results(df_cleaned, "cleaned_custom.csv")


# ============================================================================
# EXAMPLE 5: Clean and Process Results
# ============================================================================
def example_process_cleaned_data():
    """Clean data, then use it for further analysis"""
    
    cleaner = IntelligentDataCleaner(verbose=True)
    
    # Clean the data
    df = cleaner.load_data("data.csv")
    if df is None:
        return
    
    cleaner.detect_column_types(df)
    cleaner.perform_eda(df, "Dataset")
    df_cleaned = cleaner.clean_data(df)
    
    # Now use the cleaned data for your own analysis
    print("\n" + "="*60)
    print("📊 POST-CLEANING ANALYSIS")
    print("="*60)
    
    # Example: Get statistics
    numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        print(f"\n{col}:")
        print(f"  Mean: {df_cleaned[col].mean():.2f}")
        print(f"  Median: {df_cleaned[col].median():.2f}")
        print(f"  Std: {df_cleaned[col].std():.2f}")
    
    # Save
    cleaner.save_results(df_cleaned, "cleaned_data.csv")


# ============================================================================
# Run Examples
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("""
    📚 DATA CLEANING EXAMPLES
    
    Choose an example:
    1. Simple cleaning (clean one file)
    2. Batch cleaning (clean multiple files)
    3. EDA only (analyze without cleaning)
    4. Custom rules (add your own cleaning logic)
    5. Process results (use cleaned data for analysis)
    
    Usage: python examples.py 1
    """)
    
    if len(sys.argv) > 1:
        choice = sys.argv[1]
        
        if choice == "1":
            print("\n▶️  Running Example 1: Simple Cleaning")
            example_simple_cleaning()
        
        elif choice == "2":
            print("\n▶️  Running Example 2: Batch Cleaning")
            example_batch_cleaning()
        
        elif choice == "3":
            print("\n▶️  Running Example 3: EDA Only")
            example_eda_only()
        
        elif choice == "4":
            print("\n▶️  Running Example 4: Custom Rules")
            example_custom_cleaning()
        
        elif choice == "5":
            print("\n▶️  Running Example 5: Process Results")
            example_process_cleaned_data()
        
        else:
            print(f"❌ Invalid choice: {choice}")
    
    else:
        print("\n⚠️  Please provide an example number (1-5)")
