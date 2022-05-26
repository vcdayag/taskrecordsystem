# Task Record System

A simplified version of your task listing app in your phone (e.g., Samsung Notes, Google Calendar) where you can list tasks, provide grouping and deadline. That is implemented python.

## Installation

Create a virtual environment with python 3.10 .

```bash
pip install virtualenv
virtualenv -p python3.10 env
```

Activate the created virtual environment

```bash
source env/bin/activate
```

run this to check if you are using the virtual environment

```bash
which python
```

output should look like `.../trs/bin/python`

to install all of the libraries the was used.

```bash
pip install -r requirements.txt
```

### PUT THE INSTRUCTION HERE TO IMPORT THE SQL DUMP FILE PROVIDED

run this command to run the program.

```bash
python taskrecordsystem/main.py
```

## Development

`taskrecordsystem/database.py` contains all the sql related code.

`taskrecordsystem/main.py` contains the terminal ui code and user inputs.

to activate the virtual environment.

```bash
source env/bin/activate
```
run this command to run the program.

```bash
python taskrecordsystem/main.py
```

to generate a requiremnets.txt for all the libraries that was used.

```bash
pip freeze > requirements.txt
```

## Contributors

- Van Paul Angelo C. Dayag