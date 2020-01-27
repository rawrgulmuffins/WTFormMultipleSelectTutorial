WTForms Multiple Select Tutorial
============================

This is a tutorial meant to show the basics of using SQLAlchemy and WTForms to generate a basic registration page. It demos how to use WTForms to add and update a
user that is persisted in some tables with a one to many relationship

Windows Directions:

Install virtualenv
    python -m venv venv
Activate venv
    venv\scripts\activate.bat
Install libraries
    pip install -r requirements
Set flask app
    set flask_app=multiple_select
Run app
    flask run
    The app allows you to drop the db, create and seed it, add a registered user, update the user with registered_id=1

Directions For Other OS (run at your own risk):

* Install python-virtualenv
    * debian: `sudo apt-get install python-virtualenv`
    * os x: `pip install virtualenv`

* Install sqlite
    * debian: `sudo apt-get install sqlite`
    * os x: `brew install sqlite3`

* Make a virtualenv for flask projects

```
virtualenv flask
source flask/bin/activate
pip install flask
pip install flask-wtf
pip install flask-sqlalchemy
```

