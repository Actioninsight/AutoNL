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


def process_spreadsheet(spreadsheet_full_path):
    directory_path = os.path.dirname(spreadsheet_full_path)

    prompt = f"Follow these instructions to edit the input file. Create the output file to store your response. If there is no input or output, just follow the instructions. Operate in this filepath: {directory_path} Instructions: "

    # Load the spreadsheet
    df = pd.read_excel(spreadsheet_full_path)

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


def process_csv(csv_full_path):
    directory_path = os.path.dirname(csv_full_path)

    prompt = f"Follow these instructions to edit the input file. Create the output file to store your response. If there is no input or output, just follow the instructions. Operate in this filepath: {directory_path} Instructions: "
    # Load the CSV file
    df = pd.read_csv(csv_full_path)

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
        print("Usage: python main.py <path_to_file>")
        sys.exit(1)

    file_path = sys.argv[1]  # Get the file path from the command line
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in [".ods", ".xlsx", ".xls"]:
        process_spreadsheet(file_path)
    elif file_extension == ".csv":
        process_csv(file_path)
    else:
        print(f"Unsupported file type: {file_extension}")
        sys.exit(1)
