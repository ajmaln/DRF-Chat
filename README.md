# DRF-Chat
Live Chat using Django REST Framework

(_One of my just-for-fun projects_)

## Installation

This app uses memcached to store Users online status, So you will need to install it.

On Ubuntu:
```
sudo apt install memcached
```

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