# Homework2: 
Need to add `ALLOWED_HOSTS = ['.devedu.io']` and `CSRF_TRUSTED_ORIGINS = ['https://*.devedu.io']`
to the `settings.py` file, and run the server on port 3000:
```bash
python manage.py runserver 0.0.0.0:3000
```
To run a new migration: `python ./movie_theater_booking/manage.py makemigrations bookings`

## Description
This is a movie booking app.

You can login to an existing account, and create bookings based on available movies and seats.

You can access your data through the api via the /api/ pages.


## Resoures: 
https://docs.djangoproject.com/en/6.1/intro/tutorial01/ : Starting up the project

https://docs.djangoproject.com/en/6.1/topics/db/models/ : Models implimentation

https://docs.djangoproject.com/en/6.1/intro/tutorial02/ : Running first migration

https://docs.djangoproject.com/en/6.1/ref/models/fields/#django.db.models.ForeignKey : ForeignKey implimentation

https://chatgpt.com/share/6ac15e5e-4c54-83e8-bb9d-957dc7b64b34 : ChatGPT conversation

https://getbootstrap.com/docs/5.3/getting-started/introduction/ : Bootstrap CSS implimentation in base.html

https://behave-django.readthedocs.io/en/stable/: Behave test implementation

https://render.com/docs/deploy-django: Deployment

## AI Tools

Pardot : Troubleshooting server port, model creation, checking my repo, advise on next steps, help on README.

Devedu AI: Created the basic template formatting for movie_list.html, booking_history.html, and seat_booking.html 

Claude: Creating test cases for Unit, Integration, and Behave, I reviewed each test and commented functionality, adjusting each to the actual application functionality.

## Running tests
Must be in the folder containing manage.py to run the tests.

`python manage.py test`

`python manage.py behave`

## Project Structure
bookings/: Contains the app data including: migrations, templates, models, etc.

    templates/: templates used for view.py

    migrations/: chain of migrations for the sql database

features/: Contains the behave test

movie_theater_booking/: contains the project information, settings, urls, etc.



## Setup from scratch
Clone Repo: https://github.com/s-kaleb/CS4300.git

Navigate to homework2: `cd homework2`

Create Venv: 

``` 
python3 -m venv <venv name>
source <venv name>/bin/activate
pip install -r requirements.txt
```

Run the migration: `python manage.py migrate`

Create a superuser: `python manage.py createsuperuser`

Run the app: `python manage.py runserver 0.0.0.0:3000`

Run the app using gunicorn: `python -m gunicorn mysite.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000`
