import pandas as pd
import sys
import os
from dotenv import load_dotenv
from interpreter import interpreter

# Load environment variables
load_dotenv()

# Initialize the interpreter and configure it
interpreter.llm.model = os.getenv("LLM_MODEL")
interpreter.llm.temperature = 0
interpreter.llm.api_key = os.getenv("LLM_API_KEY")
interpreter.llm.api_base = os.getenv("LLM_API_BASE")
interpreter.llm.api_version = os.getenv("LLM_API_VERSION")
interpreter.auto_run = True


def process_spreadsheet(file_path):
    prompt = f"Follow these instructions to edit the input file. Create the output file to store your response. If there is no input or output, just follow the instructions. Operate in this filepath: {file_path} Instructions: "

    # Load the spreadsheet
    df = pd.read_excel(file_path)

    # Capture column names once before the loop
    column_names = df.columns

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        # Assemble a single string from the row data
        row_data_str = ", ".join(
            [
                f"{col_name}: {row[col_name]}"
                for col_name in column_names
                if pd.notna(row[col_name])
            ]
        )
        response = interpreter.chat(prompt + row_data_str)
        print(response)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_spreadsheet>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get the file path from the command line
    process_spreadsheet(file_path)
