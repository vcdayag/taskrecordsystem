# Task Record System

A simplified version of your task listing app in your phone (e.g., Samsung Notes, Google Calendar) where you can list tasks, provide grouping and deadline. That is implemented python.

## Contributors

- Van Paul Angelo C. Dayag
- Averi Cipriano

## Installation

**Make sure you have installed python and mariadb**

### Database Setup

Login using the root account and run this command.

```sql
SOURCE SQLDUMP.sql;
```

### Python Environment Setup

Create a virtual environment with python 3.10 .

```bash
pip install virtualenv
python -m virtualenv -p python3.10 env
```

Activate the created virtual environment

```bash
#in Linux
source env/bin/activate

#in Windows
source env/Scripts/activate
```

To install all of the libraries the was used.

```bash
pip install -r requirements.txt
```

**We used the python library [Rich](https://github.com/Textualize/rich) for the User Interface, Inputs, and Logging.**

This command to runs the program.

```bash
python taskrecordsystem/main.py
```

## Development

`taskrecordsystem/database.py` contains all the sql related code.

`taskrecordsystem/main.py` contains the terminal ui code and user inputs.

`taskrecordsystem/logger.py` contains the logger config and code.

Activate the virtual environment.

```bash
#in linux
source env/bin/activate

#in windows
source env/Scripts/activate
```

run this command to run the program.

```bash
python taskrecordsystem/main.py
```

to generate a requirements.txt for all the libraries that was used.

```bash
pip freeze > requirements.txt
```