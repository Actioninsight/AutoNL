# AutoNL

AutoNL helps you automate routine, well-understood tasks entirely in natural language using simple spreadsheets. 

You might find AutoNL useful if you:
   * Have to frequently repeat a series of manual steps in programs like Excel; 
   * Want to automate the preprocessing and cleaning of data without specialized software;
   * Already have all your steps and processes written down.

## How it works

AutoNL is a simple, general framework for leveraging Open-Interpreter's powerful ability to flexibly solve small tasks. Where Open-Interpreter sometimes falters is on longer, context-heavy multi-step tasks. AutoNL attempts to solve this with a carefully constructed sheet which outlines all of the processes in natural language, and manages state by additively creating new intermediate sheets so that progress is not lost upon error. With strong task articulation and steps properly broken down, processes can be solved at a high rate of reliability. 

## Warning

AutoNL is experimental and prone to failures. Use at your own risk. 

## Setup

- Install dependencies `pip install -r requirements.txt`
- Create a file called `.env`
- Copy `.env.example` keys to `.env`
- Add `.env` values

## Use

- run `python main.py <full path to spreadsheet/csv>`

## Tips

The script will create and read documents in the directory of the file you pass in.

Be sure to use the full file path.

You can drag and drop the file into Terminal to paste the path.

Be specific and use precise instructions and column references wherever possible. 

## Example 

Use autonl-example.xlsx to run a 7-step example process.

## Known Errors

Open-Interpreter will sometimes prematurely stop the generation without completing a step's task. Re-run the process to try again.
