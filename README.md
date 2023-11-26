# CISC_327_31

Group 31's repo for CISC-327

## Set up

### Install django

```bash
pip install django
```

### If you already have our repo here, delete the db.sqlite3 in Megabyte

### Once in project directory, make migrations to database

```bash
python manage.py migrate
```

### Run the program

```bash
python manage.py runserver
```

### Visit http://127.0.0.1:8000/ and register and you should be good to go!

### Testing

## Setup

In order to run the tests, Google Chrome of version 119.0.6045.105 or higher is required.
https://www.google.com/intl/en_ca/chrome/dr/download/

### Install selenium

```bash
pip install selenium
```

### Run tests

```bash
python manage.py test
```

Or the with the verbosity flag to see the status of each individual test

```bash
python manage.py test --verbosity=2
```

### Make sure you are in the project directory before running the test cases!
