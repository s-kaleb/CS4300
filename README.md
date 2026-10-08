# CS4300 Homework location

## Homework1:


## Homework2: 
Need to add `ALLOWED_HOSTS = ['.devedu.io']` and `CSRF_TRUSTED_ORIGINS = ['https://*.devedu.io']`
to the `settings.py` file inside the bookings app, and run the server on port 3000:
```bash
python manage.py runserver 0.0.0.0:3000
```
To run a new migration: `python ./movie_theater_booking/manage.py makemigrations bookings`
### Resoures: 
https://docs.djangoproject.com/en/6.1/intro/tutorial01/ : Starting up the project

https://docs.djangoproject.com/en/6.1/topics/db/models/ : Models implimentation

https://docs.djangoproject.com/en/6.1/intro/tutorial02/ : Running first migration

https://docs.djangoproject.com/en/6.1/ref/models/fields/#django.db.models.ForeignKey : ForeignKey implimentation

https://chatgpt.com/share/6ac15e5e-4c54-83e8-bb9d-957dc7b64b34 : ChatGPT conversation

https://getbootstrap.com/docs/5.3/getting-started/introduction/ : Bootstrap CSS implimentation in base.html

https://behave-django.readthedocs.io/en/stable/: Behave test implementation

### AI Tools

Pardot : Troubleshooting server port, model creation.
Devedu AI: Created the basic template formatting for movie_list.html, booking_history.html, and seat_booking.html 
Claude: Creating test cases for Unit, Integration, and Behave.

### Running tests

`python manage.py test`

`python manage.py behave`