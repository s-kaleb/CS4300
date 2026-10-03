# CS4300 Homework location


## Homework2: 
Need to add `ALLOWED_HOSTS = ['.devedu.io']` and `CSRF_TRUSTED_ORIGINS = ['https://*.devedu.io']`
to the `settings.py` file inside the bookings app, and run the server on port 3000:
```bash
python manage.py runserver 0.0.0.0:3000