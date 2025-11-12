import os
from src.data_loader import load_data, initial_analysis
try:
    from src.ai_cleaner import ai_clean
except Exception:
    # Fallback to a local deterministic cleaner if pandasai/OpenAI isn't available
    from src.ai_cleaner_local import ai_clean
    print("Using local deterministic ai_clean (fallback, no OpenAI available).")
from src.summarizer import summarize_cleaning

def run_autoetl():
    """
    Orchestrates the entire AutoETL pipeline.
    """
    print("Starting AutoETL pipeline...")
    
    # Define file path
    raw_data_path = "data/raw/messy_dataset.csv"
    
    # Step 1: Load raw data
    original_df = load_data(raw_data_path)
    
    if original_df is None:
        print("ETL process halted due to data loading failure.")
        return

    # Perform initial analysis
    initial_analysis(original_df)
    
    # Step 2: Clean data via AI agent
    try:
        cleaned_df = ai_clean(original_df.copy()) # Pass a copy to keep the original intact
    except Exception as e:
        print(f"An error occurred during the AI cleaning process: {e}")
        print("ETL process halted.")
        return
        
    # Step 3: Summarize results
    print("\nFinal Cleaned DataFrame info:")
    cleaned_df.info()
    print("\nFinal Cleaned DataFrame head:")
    print(cleaned_df.head())
    
    summarize_cleaning(original_df, cleaned_df)
    
    print("\nAutoETL pipeline completed successfully!")

if __name__ == "__main__":
    # Check for .env file for API key
    if not os.path.exists(".env"):
        print("Warning: .env file not found.")
        print("Please create a .env file in the root directory with your OPENAI_API_KEY.")
        # Example for creating the .env file
        with open(".env.example", "w") as f:
            f.write("OPENAI_API_KEY=\"your_api_key_here\"\n")
        print("An '.env.example' file has been created. Please rename it to '.env' and add your key.")
    else:
        run_autoetl()
