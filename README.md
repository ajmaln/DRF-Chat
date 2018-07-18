# DRF-Chat
Live Chat using Django REST Framework

## Installation

Install virtualenv
```
pip install virtualenv
```
On the project directory,

Create virtual environment
```
virtualenv venv
```
Activate
```
source venv/bin/activate
```

Install requirements
```
pip install -r requirements.txt
```

Do Database migrations
```
./manage.py makemigrations
./manage.py makemigrations chat
./manage.py migrate
```

Try creating a superuser for user management
```
./manage.py createsuperuser
```

Give necessary inputs

Run development server

```
./manage.py runserver
```
