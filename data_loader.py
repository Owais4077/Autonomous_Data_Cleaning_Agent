import pandas as pd

def load_data(file_path):
    """
    Loads a CSV file into a pandas DataFrame and prints basic info.
    """
    print(f"Loading data from {file_path}...")
    try:
        df = pd.read_csv(file_path)
        print("Data loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None

def initial_analysis(df):
    """
    Performs an initial analysis of the DataFrame.
    """
    if df is not None:
        print("\nInitial DataFrame info:")
        df.info()
        print("\nInitial DataFrame head:")
        print(df.head())
        print("\nMissing values before cleaning:")
        print(df.isnull().sum())
        print(f"\nNumber of duplicate rows before cleaning: {df.duplicated().sum()}")

if __name__ == '__main__':
    # This block is for testing the data_loader module directly
    raw_data_path = "data/raw/messy_dataset.csv"
    dataframe = load_data(raw_data_path)
    initial_analysis(dataframe)
