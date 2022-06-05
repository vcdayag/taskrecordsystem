# Task Record System

A simplified version of your task listing app in your phone (e.g., Samsung Notes, Google Calendar) where you can list tasks, provide grouping and deadline, that is implemented python.

## Contributors

- Van Paul Angelo C. Dayag
- Averi Cipriano

## Installation

**Make sure you have installed Python and MariaDB**

### Database Setup

Login using the root account and run this commands.

```sql
CREATE USER IF NOT EXISTS 'tsruser'@'localhost' IDENTIFIED BY 'tsrpassword'; 
CREATE DATABASE IF NOT EXISTS taskrecordsystem;
GRANT ALL ON taskrecordsystem.* TO 'tsruser'@'localhost';
USE taskrecordsystem;
SOURCE TSR.sql;
```

### Python Environment Setup

Create a virtual environment with Python 3.10

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

To install all of the libraries that was used. **We used the python library [Rich](https://github.com/Textualize/rich) for the user interface, inputs, and logging.**

```bash
pip install -r requirements.txt
```



This command to runs the program.

```bash
python taskrecordsystem/main.py
```

## Development

`taskrecordsystem/database.py` contains all the database queries, and sql related code.

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