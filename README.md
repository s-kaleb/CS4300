# CS4300 Homework location

## Homework1:


## Homework2: 
Need to add `ALLOWED_HOSTS = ['.devedu.io']` and `CSRF_TRUSTED_ORIGINS = ['https://*.devedu.io']`
to the `settings.py` file inside the bookings app, and run the server on port 3000:
```bash
python manage.py runserver 0.0.0.0:3000
```
### Resoures: 
https://docs.djangoproject.com/en/6.1/intro/tutorial01/ : Starting up the project

Pardot : Troubleshooting server port, model creation.

https://docs.djangoproject.com/en/6.1/topics/db/models/ : Models implimentation

https://docs.djangoproject.com/en/6.1/ref/models/fields/#django.db.models.ForeignKey : ForeignKey implimentation

https://chatgpt.com/share/6ac15e5e-4c54-83e8-bb9d-957dc7b64b34 : ChatGPT conversation