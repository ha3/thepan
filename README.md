# thepan

thepan is a web application that lets you search recipes by ingredients.

## Installation
Start with activating virtualenv.

OS X & Linux:

```bash
$ python3.6 -m venv venv
$ . venv/bin/activate
```

Windows:

```bash
> python -m venv venv
> venv/Scripts/activate
```

Then, install dependencies and migrate.

```bash
pip install -r requirements.txt
python manage.py migrate
```

## Usage

```bash
python manage.py runserver
```

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
