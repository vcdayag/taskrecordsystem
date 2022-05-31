# Task Record System

A simplified version of your task listing app in your phone (e.g., Samsung Notes, Google Calendar) where you can list tasks, provide grouping and deadline. That is implemented python.

## Installation

**Make sure you have installed python and mariadb**

Create a virtual environment with python 3.10 .

```bash
pip install virtualenv
python -m virtualenv -p python3.10 env
```

Activate the created virtual environment

```bash
source env/Scripts/activate
```

run this to check if you are using the virtual environment

```bash
which python
```

output should look like `.../env/Scripts/python`

to install all of the libraries the was used.

```bash
pip install -r requirements.txt
```

**We used the python library [Rich](https://github.com/Textualize/rich) for the User Interface, Inputs, and Logging.**

for the database we must set the username and password inorder to access the database

```bash
EXAMPLE
dotenv set TSRUSER root
dotenv set TSRPASSWORD password
```

Then run `dotenv list` to check if it is correctly set it should display like this

```bash
TSRUSER=root
TSRPASSWORD=password
```

### PUT THE INSTRUCTION HERE TO IMPORT THE SQL DUMP FILE PROVIDED

run this command to run the program.

```bash
python taskrecordsystem/main.py
```

## Development

`taskrecordsystem/database.py` contains all the sql related code.

`taskrecordsystem/main.py` contains the terminal ui code and user inputs.

`taskrecordsystem/logger.py` contains the logger config and code.

to activate the virtual environment.

```bash
source env/Scripts/activate
```
run this command to run the program. Don't forget to change the password according to your mysql root password.

```bash
python taskrecordsystem/main.py
```

to generate a requirements.txt for all the libraries that was used.

```bash
pip freeze > requirements.txt
```

## Contributors

- Van Paul Angelo C. Dayag