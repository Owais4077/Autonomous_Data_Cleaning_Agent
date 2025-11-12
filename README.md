# Autonomous Data Cleaning Agent

This project is an AI-powered system that takes a messy CSV file as input, automatically detects and cleans data inconsistencies, and generates a summarized report.

## AI Workflow

The agent uses PandasAI and the OpenAI GPT-4 Turbo model to intelligently clean the data. The process is as follows:

1.  **Load Data**: The raw, messy CSV is loaded into a Pandas DataFrame.
2.  **AI Cleaning**: A `SmartDataframe` object from PandasAI is created, configured with the OpenAI LLM. The agent is prompted to clean the dataset, fix missing values, and standardize formats.
3.  **Summarize**: A report is generated detailing the cleaning actions taken, along with a visual comparison of missing values before and after cleaning.
4.  **Save**: The cleaned DataFrame is saved to a new CSV file.

## How to Run

1.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  Create a `.env` file in the root directory and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your_api_key_here"
    ```

3.  Run the AutoETL pipeline:
    ```bash
    python src/autoetl_agent.py
    ```

## Expected Outputs

-   A cleaned dataset will be saved to `data/cleaned/cleaned_dataset.csv`.
-   A text summary of the cleaning process will be saved to `reports/cleaning_summary.txt`.
-   A visual summary of missing values will be saved to `reports/visual_summary.png`.
