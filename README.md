WTForms Multiple Select Tutorial
============================

This is a tutorial meant to show the basics of using SQLAlchemy and WTForms to generate a basic registration page. There's a lot to this tutorial but you should be able to get it up and running after following these basic steps. It should be noted that this tutorial was run on Ubuntu 13.10 and freebsd. Windows and OSX at your own risk.

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

