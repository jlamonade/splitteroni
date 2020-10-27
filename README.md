# Splitteroni

This is a simple no non-sense bill splitter web app that I created because I didn't like the other bill splitter apps currently available.

## Running the project

1. Clone this repo to `~/splitteroni`
1. Install dependencies: `pipenv install`
1. Create a virtual environment: `virtualenv venv -p python3.8`
1. Activate the environment: `. venv/bin/activate`
1. Update config/settings.py by adding your own django secret key
1. Start Django internal test server: `python manage.py runserver`
1. Create the superuser: `python manage.py createsuperuser`
1. Make the first migration: `python manage.py migrate`

## Non-pip dependencies

- `python3.8`
- `postgresql`

## Deployment

- Prior to deployment you'll need to enter your own django secret key into docker-compose-public.yml
```
environment:
  "DJANGO_SECRET_KEY=enter_key_here"
```
