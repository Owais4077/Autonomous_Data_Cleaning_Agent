import os
import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI
from dotenv import load_dotenv

def ai_clean(df):
    """
    Cleans the DataFrame using PandasAI with OpenAI GPT-4 Turbo.
    """
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY not found. Please create a .env file and add your API key.")

    print("\nInitializing AI data cleaning process...")
    
    llm = OpenAI(api_token=api_key)
    sdf = SmartDataframe(df, config={"llm": llm})

    # Prompt for cleaning the data
    cleaning_prompt = (
        "Clean this dataset by performing the following actions: "
        "1. Identify and fill missing 'Age' values using the median age. "
        "2. Identify and fill missing 'Salary' values using the mean salary for the respective 'City'. "
        "3. Correct inconsistent capitalization in the 'City' column (e.g., 'new york' should be 'New York'). "
        "4. Ensure the 'Joining_Date' column is in a consistent 'YYYY-MM-DD' format. "
        "5. Remove any duplicate rows."
    )
    
    print("Sending cleaning prompt to the AI...")
    cleaned_df = sdf.chat(cleaning_prompt)
    
    if isinstance(cleaned_df, pd.DataFrame):
        print("AI cleaning process completed successfully.")
        # Save the cleaned data
        output_path = "data/cleaned/cleaned_dataset.csv"
        cleaned_df.to_csv(output_path, index=False)
        print(f"Cleaned data saved to {output_path}")
        return cleaned_df
    else:
        print("Warning: AI cleaning did not return a DataFrame. Returning original DataFrame.")
        # In case the response is not a dataframe, which can happen.
        print("AI Response:", cleaned_df)
        return df

if __name__ == '__main__':
    # This block is for testing the ai_cleaner module directly
    from data_loader import load_data
    
    raw_data_path = "data/raw/messy_dataset.csv"
    dataframe = load_data(raw_data_path)
    
    if dataframe is not None:    python run_pipeline.py --input data/raw/your_dataset.csv
        cleaned_dataframe = ai_clean(dataframe)
        print("\nCleaned DataFrame head:")
        print(cleaned_dataframe.head())
