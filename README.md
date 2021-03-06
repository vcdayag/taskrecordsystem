# Task Record System

A simplified version of your task listing app in your phone (e.g., Samsung Notes, Google Calendar) where you can list tasks, provide grouping and deadline, that is implemented python.

## Contributors

- Van Paul Angelo C. Dayag
- Zenith Averi V. Cipriano

## Installation

**Make sure you have installed Python and MariaDB**

### Database Setup

Login using the root account and run this commands. **The MariaDB instance should be hosted on 127.0.0.1 port 3306**

```sql
CREATE USER IF NOT EXISTS 'trsuser'@'localhost' IDENTIFIED BY 'trspassword';
CREATE DATABASE IF NOT EXISTS taskrecordsystem;
GRANT ALL ON taskrecordsystem.* TO 'trsuser'@'localhost';
USE taskrecordsystem;
SOURCE TRS.sql;
```

### Python Environment Setup

Create a virtual environment with Python3.10. **at least version 3.10 of Python is necessary because we used some functions that are first introduced in this version.**

```bash
pip install virtualenv
python -m virtualenv -p python3.10 env
```

Activate the created virtual environment.

```bash
#in Linux
source env/bin/activate

#in Windows must use Command Prompt
.\env\Scripts\activate.bat
# if successful the path should look something like this
# (env) C:\...\taskrecordsystem-main>
```

Install all of the libraries that was used. **We used the python library [Rich](https://github.com/Textualize/rich) for the user interface, inputs, and logging.**

```bash
pip install -r requirements.txt
```

This command runs the program.

```bash
python taskrecordsystem/main.py
```

## Development

`taskrecordsystem/database.py` contains all the database queries, and sql related code.

`taskrecordsystem/main.py` contains the terminal ui code and user inputs.

`taskrecordsystem/logger.py` contains the logger config and code.

Activate the virtual environment.

```bash
#in Linux
source env/bin/activate

#in Windows must use Command Prompt
.\env\Scripts\activate.bat
# if successful the path should look something like this
# (env) C:\...\taskrecordsystem-main>
```

This command runs the program.

```bash
python taskrecordsystem/main.py
```

to generate a requirements.txt for all the libraries that was used.

```bash
pip freeze > requirements.txt
```
