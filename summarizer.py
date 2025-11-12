import matplotlib.pyplot as plt
import pandas as pd

def summarize_cleaning(original_df, cleaned_df):
    """
    Generates a text and visual summary of the data cleaning process.
    """
    print("\nGenerating cleaning summary report...")

    # 1. Text Summary
    original_rows, original_cols = original_df.shape
    cleaned_rows, cleaned_cols = cleaned_df.shape
    
    duplicates_removed = original_df.duplicated().sum()
    
    original_missing = original_df.isnull().sum()
    cleaned_missing = cleaned_df.isnull().sum()
    
    summary_text = (
        "=======================================\n"
        "      Data Cleaning Summary Report     \n"
        "=======================================\n\n"
        f"Original Dataset Dimensions: {original_rows} rows, {original_cols} columns\n"
        f"Cleaned Dataset Dimensions:  {cleaned_rows} rows, {cleaned_cols} columns\n\n"
        f"Duplicate Rows Removed: {duplicates_removed}\n\n"
        "Missing Values Analysis:\n"
        "------------------------\n"
        "Column          | Before | After\n"
        "----------------|--------|------\n"
    )

    for col in original_missing.index:
        summary_text += f"{col:<15} | {original_missing[col]:<6} | {cleaned_missing[col]:<5}\n"

    summary_text += "\nCleaning Actions:\n"
    summary_text += "- Handled missing values in 'Age' and 'Salary' columns.\n"
    summary_text += "- Standardized capitalization in the 'City' column.\n"
    summary_text += "- Ensured 'Joining_Date' is in a consistent format.\n"
    summary_text += "- Removed duplicate records.\n"

    # Save text summary
    report_path = "reports/cleaning_summary.txt"
    with open(report_path, "w") as f:
        f.write(summary_text)
    print(f"Text summary saved to {report_path}")

    # 2. Visual Summary
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    
    # Before
    original_missing.plot(kind='bar', ax=ax1, color='salmon')
    ax1.set_title('Missing Values Before Cleaning')
    ax1.set_ylabel('Number of Missing Values')
    ax1.tick_params(axis='x', rotation=45)
    
    # After
    cleaned_missing.plot(kind='bar', ax=ax2, color='lightgreen')
    ax2.set_title('Missing Values After Cleaning')
    ax2.set_ylabel('Number of Missing Values')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save visual summary
    visual_report_path = "reports/visual_summary.png"
    plt.savefig(visual_report_path)
    print(f"Visual summary saved to {visual_report_path}")
    # plt.show()

if __name__ == '__main__':
    # Example usage for testing
    # Create dummy dataframes to test the summarizer
    data_before = {
        'A': [1, 2, None, 4, 1],
        'B': ['x', 'y', 'z', 'y', 'x'],
        'C': [None, None, 3, 4, 5]
    }
    df_before = pd.DataFrame(data_before)
    
    data_after = {
        'A': [1, 2, 2.5, 4, 1],
        'B': ['X', 'Y', 'Z', 'Y', 'X'],
        'C': [3.5, 3.5, 3, 4, 5]
    }
    df_after = pd.DataFrame(data_after)
    
    summarize_cleaning(df_before, df_after)
