# pizza-constructor

## How to run the project

1. Create `pizza_constructor/local_settings.py` file and specify the next variables inside it:

    `EMAIL_USE_SSL = True`
    
    `EMAIL_PORT = 465`
    
    or
    
    `EMAIL_USE_TLS = True`
    
    `EMAIL_PORT = 587`
    
    and
    
    `EMAIL_HOST = 'smtp.<server_domain>'`
    
    `EMAIL_HOST_USER = '<email_address>@<server_domain>'`
    
    `EMAIL_HOST_PASSWORD = '<password>'`

1. `python3 -m venv env`
1. `source env/bin/activate`
1. `pip install -r requirements.txt`
1. `python3 manage.py migrate`
1. `python3 manage.py createsuperuser`
1. `python3 manage.py runserver`

Now you can send a pizza order form via a main page and CRUD ingredients and their groups via Django admin panel.
