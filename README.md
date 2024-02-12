# AutoNL

Use natural language instructions to automate tasks. 

## Warning

AutoNL is experimental and prone to failures. Use at your own risk. 

## Setup

- Install dependencies `pip install -r requirements.txt`
- Create a file called `.env`
- Copy `.env.example` keys to `.env`
- Add `.env` values

## Use

- run `python main.py <path to spreadsheet/csv>`

## Tips

The script will create and read documents in the directory of the file you pass in.

You can drag and drop the file into Terminal to paste the path.

Be specific and use precise instructions and column references wherever possible. 

## Example 

Use autonl-example.xlsx to run a 7-step example process.

## Known Errors

Open-Interpreter will sometimes prematurely stop the generation without completing a step's task. Watch for this. 
