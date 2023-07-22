# Stack for Django Projects by Miguel Polo

## Features

- Swagger and postman are used for documentation

## Requirements

- Docker
- docker-compose

## Run

### Setup

1. Clone repository:

- `git clone git@github.com:miguepoloc/django_stack.git`

- `cd django_stack`

### Run With Docker

2. Copy `.env.example` to `.env` and custom:

- `cp .env.example .env`

3. docker-compose

- `sudo docker-compose -f docker-compose.dev.yml build`

- `sudo docker-compose -f docker-compose.dev.yml up`

### Run With Virtualenv

1. Copy `.env.example` to `.env` and custom:

- `cp .env.example .env`

1. Create virtualenv and activate

- `python -m venv venv`
- `source venv/bin/activate` _(Linux)_
- `./venv/Scripts/activate` _(Windows)_

4. Install requirements

- `pip install -r /requirements/dev.txt`

1. Run

- `cd src`
- `python manage.py runserver`

## Migrations With Docker

### With Docker

- `sudo docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py makemigrations"`

- `sudo docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py migrate"`

### With Virtualenv

- `cd src`
- `python manage.py makemigrations`
- `python manage.py migrate`

## Create new app

### With Docker

- `sudo docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py startapp appname"`

### With Virtualenv

- `cd src`
- `python manage.py startapp appname`

## Test

### With Docker

- `sudo docker-compose -f docker-compose.dev.yml run --rm django sh -c "python manage.py test"`

### With Virtualenv

- `cd src`
- `python manage.py test`

## Linter
Use pre-commit to run linter before commit, the command is:
- `pre-commit run --all-files`
