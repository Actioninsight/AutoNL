import pandas as pd
import sys
import os
import time
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
interpreter.llm.context_window = os.getenv("CONTEXT_WINDOW")
interpreter.system_message = "You are Open Interpreter, a world-class programmer that can complete any goal by executing code. When you execute code, it will be executed **on the user's machine**. The user has given you **full and complete permission** to execute any code necessary to complete the task. Execute the code. If you want to send data between programming languages, save the data to a txt or json. You can access the internet. Run **any code** to achieve the goal, and if at first you don't succeed, try again and again. You can install new packages. When a user refers to a filename, they're likely referring to an existing file in the directory you're currently executing code in. Write messages to the user in Markdown. You are capable of **any** task. NEVER PLAN! Trust the user's instructions and complete the task with code immediately. [User Info] {{import getpass import os import platform}} Name: {{getpass.getuser()}} CWD: {{os.getcwd()}} SHELL: {{os.environ.get('SHELL')}} OS: {{platform.system()}}"
interpreter.custom_instructions = "If you need to install a python library, you must use `python -m pip install <library>` because you don't know what environment you're running in. We've already figured out the master plan and we just want you to focus on nailing, efficiently and accurately, this simple instruction we've provided for this one single step. You can nail it in one shot, no problem. Try to do the whole step in one coding flow. If someone has given you precise column details, use them. If they've only given you vague references, first read the file. Once the code has executed and the file has been saved, just print something very short and brief like 'The file ____ was saved successfully.' Do not summarize or give an overview on what has been done. When you are done, save all code you ran as stepX.py, where X is the step number you're on. thank you!"


def process_spreadsheet(spreadsheet_full_path):
    directory_path = os.path.dirname(spreadsheet_full_path) 

    prompt = (
        "Your job is to execute instructions in a spreadsheet.\n"
        "There will be an input file that contains the data you operate on.\n"
        "You will always store the results of your work to the output file. *Never* overwrite existing files.\n"
        "If there is no input or output, just follow the instructions. Credentials will be provided to you via system environment variables that look like this 'BOT_PASSWORD'.\n"
        f"Operate in this filepath: '{directory_path}'\n"
        "Instructions: "
    )
    # Load the spreadsheet
    df = pd.read_excel(spreadsheet_full_path)

    # Capture column names once before the loop
    column_names = df.columns

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        start_time = time.time()
        current_row = index + 1
        interpreter.messages = []
        try:
            print(f"***** Executing instruction {current_row} of {len(df)} *****")
            # Assemble a single string from the row data
            row_data_str = ", ".join(
                [
                    f"{col_name}: {row[col_name]}"
                    for col_name in column_names
                    if pd.notna(row[col_name])
                ]
            )
            print(f"Row data: {row_data_str}")

            # Execute the instruction
            response = interpreter.chat(prompt + row_data_str)
            print(response)

            validation_prompt = (
                "You have just finished executing an instruction. "
                f"You must validate that the output was successfully created in {directory_path}. "
                "If there is an issue, you must fix the problem and re-run the instruction.\n"
                "Here are the instructions: "
            )
            validation_response = interpreter.chat(
                validation_prompt + " " + row_data_str
            )
            print(validation_response)

            # Log the time after processing the row
            end_time = time.time()
            print(
                f"***** Time taken for instruction {current_row}: {end_time - start_time:.2f} seconds *****"
            )

        except KeyboardInterrupt:
            print("***** KeyboardInterrupt caught, breaking out of the loop. *****")
            sys.exit(0)  # Exit the program
        except Exception as e:
            print(f"***** Error on instruction {current_row}: {e} *****")

    # Validate the spreadsheet execution
    validation_prompt = f"You have just finished iterating through a list of instructions in a spreadsheet. You must validate that the outputs in the spreadsheet were successfully created in {directory_path}. Hash each of these files and store their hashes in runhash.txt. Move all the files, including runhash.txt to a new, timestamped folder in this directory in this format e.g. '20240214112154' and rename runhash.txt to the folder name. Here are the instructions: "

    spreadsheet_data = ", ".join([str(row) for index, row in df.iterrows()])

    print("***** Validating output... *****")
    validation_response = interpreter.chat(validation_prompt + " " + spreadsheet_data)
    print(validation_response)


def process_csv(csv_full_path):
    directory_path = os.path.dirname(csv_full_path)

    prompt = (
        "Your job is to execute instructions in a CSV file.\n"
        "There will be an input file that contains the data you operate on.\n"
        "You will store the results of your work to the output file.\n"
        "If there is no input or output, just follow the instructions.\n"
        f"Operate in this filepath: '{directory_path}'\n"
        "Instructions: "
    )
    # Load the CSV file
    df = pd.read_csv(csv_full_path)

    # Capture column names once before the loop
    column_names = df.columns

    try:
        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            start_time = time.time()
            current_row = index + 1
            interpreter.messages = []
            # Assemble a single string from the row data
            row_data_str = ", ".join(
                [
                    f"{col_name}: {row[col_name]}"
                    for col_name in column_names
                    if pd.notna(row[col_name])
                ]
            )
            print(f"***** Executing instruction {current_row} of {len(df)} *****")
            print(f"Row data: {row_data_str}")

            # Execute the instruction
            response = interpreter.chat(prompt + row_data_str)
            print(response)

            validation_prompt = (
                "You have just finished executing an instruction. "
                f"You must validate that the output was successfully created in {directory_path}."
                "If there is an issue, you must fix the problem and re-run the instruction.\n"
                "Here are the instructions:"
            )
            validation_response = interpreter.chat(
                validation_prompt + " " + row_data_str
            )
            print(validation_response)

            # Log the time after processing the row
            end_time = time.time()
            print(
                f"***** Time taken for instruction {current_row}: {end_time - start_time:.2f} seconds *****"
            )

    except KeyboardInterrupt:
        print("***** KeyboardInterrupt caught, exiting the loop. *****")
        sys.exit(0)  # Exit the program
    except Exception as e:
        print(f"***** Error on instruction {current_row}: {e} *****")

    # Validate the CSV execution
    validation_prompt = f"You have just finished iterating through a list of instructions in a CSV file. You must validate that the outputs in the CSV were successfully created in {directory_path}. Here are the instructions:"

    csv_data = ", ".join([str(row) for index, row in df.iterrows()])

    print("***** Validating output... *****")
    validation_response = interpreter.chat(validation_prompt + " " + csv_data)
    print(validation_response)


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
