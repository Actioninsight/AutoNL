# AutoNL

Use natural language instructions to automate tasks.

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

You can create an alias such as `alias autonl="python main.py"` and then run `autonl <path to spreadsheet/csv>`
