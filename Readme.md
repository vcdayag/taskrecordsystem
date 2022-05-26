# How to run

`pip install virtualenv`

create a virtual environment with python 3.10

`virtualenv -p python3.10 trs`

to activate the virtual environment

`source trs/bin/activate`

run this to check if you are using the virtual environment

`which python`

output should look like `.../trs/bin/python`

to install all of the libraries the was used.

`pip install -r requirements.txt`

# Development

to generate a requiremnets.txt for all the libraries that was used.

`pip freeze > requirements.txt`