"""
This tutorial is meant to be read from top to bottom, with comments explaining
what each section does and why it's there.

Please note, this file doesn't contain very good software engineering practices
This is supposed to be used for demonstrating purposes only.

If you want to see how you should structure a flask application so that you
don't get bogged down with needless code complexity head on over to.
http://flask.pocoo.org/docs/patterns/packages/

NOTE: If you want another flask tutorial you should head on over to
http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

Author: Alex Lord
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

"""
Need to configure our application and the database connection. In most cases
you probably want to load all of this from a configuration file.

In this tutorial we're just going to use a basic sqlalchemy test database.
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Insert_random_string_here'
#Set this configuration to True if you want to see all of the SQL generated.
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basic_app3.sqlite'

#WTForms configuration strings
app.config['WTF_CSRF_ENABLED'] = True
#CSRF tokens are important. Read more about them here,
#https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet
app.config['WTF_CSRF_SECRET_KEY'] = 'Insert_random_string_here'
db = SQLAlchemy(app)

# --------------------- should be in a models package -- ---------------------

"""
Next we need to create our model classes that will be used during the creation
of the database and also when we want to manipulate the database. This should
normally be it's own seperate file.

I'm importanting from here as if this was it's own seperate file.

Normally you'd have to import doing something like
from application import db
"""

class RegisteredUser(db.Model):
    """
    loads and pushes registered user data after they have signed up.

    SQLalchemy ORM table object which is used to load, and push, data from the
    server memory scope to, and from, the database scope.
    """
    __tablename__ = "RegisteredUser"

    #all of the columns in the database.
    registered_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(70))
    last_name = db.Column(db.String(70))
    address_line_one = db.Column(db.String(256))
    address_line_two = db.Column(db.String(256))
    city = db.Column(db.String(50))

    """
    Now we're going to create all of the foreign keys for the RegisteredUser
    table. The db.relationship section allows us to easily and automatically
    join the other tables with registeredUser. The Join will only take place
    if you attempt to access columns from the State or country table.

    For more on Foreign keys using SQLAlchemy go to
    """
    state_id = db.Column(
            db.Integer,
            db.ForeignKey('State.state_id'),
            nullable=False)
    #retrives the users name for display purposes.
    state_by = db.relationship(
            'State',
            foreign_keys=[state_id],
            backref=db.backref('State', lazy='dynamic'))
    country_id = db.Column(
            db.Integer,
            db.ForeignKey('Country.country_id'),
            nullable=False)
    #retrives the users name for display purposes.
    country_by = db.relationship(
            'Country',
            foreign_keys=[country_id],)

    #this is the method and function style I've chosen when lines are too long
    def __init__(
            self,
            first_name,
            last_name,
            address_line_one,
            address_line_two,
            city,
            state_id,
            country_id):
        """
        Used to create a RegisteredUser object in the python server scope

        We will be calling these init functions every time we use
        RegisteredUser() as a 'function' call. It will create a SQLalchemy ORM
        object for us.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.address_line_one = address_line_one
        self.address_line_two = address_line_two
        self.city = city
        self.state_id = state_id
        self.country_id = country_id


class State(db.Model):  # pylint: disable-msg=R0903
    """
    Holds State names for the database to load during the registration page.

    SQLalchemy ORM table object which is used to load, and push, data from the
    server memory scope to, and from, the database scope.
    """
    __tablename__ = "State"

    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(10), unique=True)

    def __init__(self, state_name):
        """
        Used to create a State object in the python server scope
        """
        self.state_name = state_name


class Country(db.Model):  # pylint: disable-msg=R0903
    """
    Holds Country names for the database to load during the registration page.

    SQLalchemy ORM table object which is used to load, and push, data from the
    server memory scope to, and from, the database scope.
    """
    __tablename__ = "Country"

    country_id = db.Column(db.Integer, primary_key=True)
    #longest country length is currently 163 letters
    country_name = db.Column(db.String(256), unique=True)

    def __init__(self, country_name):
        """
        Used to create a Country object in the python server scope
        """
        self.country_name = country_name


def create_example_data():
    """
    Generates all of the demo data to be used later in the tutorial. This is
    how we can use our ORM objects to push data to the database.

    NOTE: create_example_data is called at the very bottom of the file.
    """
    #Create a bunch of state models and add them to the current session.
    #Note, this does not add rows to the database. We'll commit them later.
    state_model = State(state_name="WA")
    db.session.add(state_model)
    state_model = State(state_name="AK")
    db.session.add(state_model)
    state_model = State(state_name="LA")
    db.session.add(state_model)
    #Normally I load this data from very large CVS or json files and run This
    #sort of thing through a for loop.

    country_model = Country("USA")
    db.session.add(country_model)
    country_model = Country("Some_Made_Up_Place")
    db.session.add(country_model)
    # Interesting Note: things will be commited in reverse order from when they
    # were added.
    try:
        db.session.commit()
    except IntegrityError as e:
        print("attempted to push data to database. Not first run. continuing\
                as normal.")

# --------------------- should be in a models package --- ---------------------

# ------------------------ should be in a forms package -----------------------
"""
Now we're going to make our WTForms objects. These will have the data aquired
from the database placed on them, then we will pass them to our template files
where we will render them.

I'm importanting from here as if this was it's own seperate file.
"""
import wtforms
import wtforms.validators as validators
from flask_wtf import Form

class RegistrationForm(Form):
    """
    This Form class contains all of the fileds that make up our registration
    Form. 
    """
    #Get all of the text fields out of the way.
    first_name_field = wtforms.TextField(
            label="First Name",
            validators=[validators.Length(max=70), validators.Required()])
    last_name_field = wtforms.TextField(
            label="Last Name",
            validators=[validators.Length(max=70), validators.Required()])
    address_line_one_field = wtforms.TextField(
            label="Address",
            validators=[validators.Length(max=256), validators.Required()])
    address_line_two_field = wtforms.TextField(
            label="Second Address",
            validators=[validators.Length(max=256), ])
    city_field = wtforms.TextField(
            label="City",
            validators=[validators.Length(max=50), validators.Required()])
    # Now let's set all of our select fields.
    state_select_field = wtforms.SelectField(label="State", coerce=int)
    country_select_field = wtforms.SelectField(label="Country", coerce=int)

# ------------------------ should be in a forms package -----------------------

#this should be in a file I normally call views.py
import flask

def populate_form_choices(registration_form):
    """
    Pulls choices from the database to populate our select fields.
    """
    states = State.query.all()
    countries = Country.query.all()
    state_names = []
    for state in states:
        state_names.append(state.state_name)
    #choices need to come in the form of a list comprised of enumerated lists
    #example [('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    state_choices = list(enumerate(state_names,start=1))
    country_names = []
    for country in countries:
        country_names.append(country.country_name)
    country_choices = list(enumerate(country_names,start=1))
    print('country choices:', country_choices)
    #now that we've built our choices, we need to set them.
    registration_form.state_select_field.choices = state_choices
    registration_form.country_select_field.choices = country_choices

@app.route('/demonstration', methods=['GET', 'POST'])
def demonstration():
    """
    This will render a template that displays all of the form objects if it's
    a Get request. If the use is attempting to Post then this view will push
    the data to the database.
    """
    #this parts a little hard to understand. flask-wtforms does an implicit
    #call each time you create a form object. It attempts to see if there's a
    #request.form object in this session and if there is it adds the data from
    #the request to the form object.
    registration_form = RegistrationForm()
    #Before we attempt to validate our form data we have to set our select
    #field choices. This is just something you need to do if you're going to 
    #use WTForms, even if it seems silly.
    populate_form_choices(registration_form)
    #This means that if we're not sending a post request then this if statement
    #will always fail. So then we just move on to render the template normally.
    if flask.request.method == 'POST' and registration_form.validate():
        #If we're making a post request and we passed all the validators then
        #create a registered user model and push that model to the database.
        print("DEBUGGGGG")
        registered_user = RegisteredUser(
            first_name=registration_form.data['first_name_field'],
            last_name=registration_form.data['last_name_field'],
            address_line_one=registration_form.data['address_line_one_field'],
            address_line_two=registration_form.data['address_line_two_field'],
            city=registration_form.data['city_field'],
            state_id=registration_form.data['state_select_field'],
            country_id=registration_form.data['country_select_field'],)
        db.session.add(registered_user)
        db.session.commit()
        print("DEBUGGGGGENDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD")
        flask.flash("This data was saved to the database!")
        return flask.redirect(flask.url_for(
            'user_detail',user_id=registered_user.registered_id))
    return flask.render_template(
            template_name_or_list='registration.html',
            registration_form=registration_form,)
"""
More lengthy explanation of what happens in above function:
1)Instantiate form (registration_form)
2)The basic instantiated form doesn't have the country and states in the select lists so add those using 
the custom populate_form_choices method.
If GET:
3) Render form in the template
If POST:
3) Using the RegisteredUser Model instantiate a new  registered_user object using data from registration_form  
(In simple cases this could be done with the populate_obj method like so:
registration_form.populate_obj(registered_user).  But according to the WTForms documentation this is only 
advisable with simple cases.)
4) Run your sqlalchemy add and commit methods to save the updated registered_user object back to the db.
"""

@app.route('/update_user/<user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    """
    This will render a template that displays all of the form objects if it's
    a Get request. If the use is attempting to Post then this view will push
    the data to the database.
    """
    #instantiate the user you want to update
    reg_user = RegisteredUser.query.filter(RegisteredUser.registered_id == user_id).first()
    #instantiate the form and populate it with values from the instantiated user
    registration_form = RegistrationForm(
        first_name_field=reg_user.first_name,
        last_name_field=reg_user.last_name,
        address_line_one_field=reg_user.address_line_one,
        address_line_two_field=reg_user.address_line_two,
        city_field=reg_user.city,
        state_select_field=reg_user.state_id,
        country_select_field=reg_user.country_id
    )
    #the form includes some drop downs for selecting states and countries. this function adds these to the form
    populate_form_choices(registration_form)

    if flask.request.method == 'POST' and registration_form.validate():
        #If we're making a post request and we passed all the validators then
        #update the instantiated registered user model from the form and push that model to the database.
        reg_user = RegisteredUser.query.filter(RegisteredUser.registered_id == user_id).first()
        reg_user.first_name=str(registration_form.data['first_name_field'])
        reg_user.last_name=registration_form.data['last_name_field']
        reg_user.address_line_one=registration_form.data['address_line_one_field']
        reg_user.address_line_two=registration_form.data['address_line_two_field']
        reg_user.city=registration_form.data['city_field']
        reg_user.state_id=registration_form.data['state_select_field']
        reg_user.country_id=registration_form.data['country_select_field']
        db.session.add(reg_user)
        db.session.commit()
        flask.flash("This data was updated to the database!")
        return flask.redirect(flask.url_for(
            'user_detail',user_id=reg_user.registered_id))
    return flask.render_template(
            template_name_or_list='update_user.html',
            registration_form=registration_form,)



@app.route('/user/<user_id>')
def user_detail(user_id):
    user = RegisteredUser.query.get_or_404(user_id)
    return flask.render_template(
        template_name_or_list='success.html',
        user=user)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/create_all')
def create_all():
    db.create_all()
    create_example_data()
    message = "DB Created! (A SQLite DB File Should Appear In Your Project Folder.  " \
              "Also, if changes are made to the model, running this again should " \
              "add these changes to the db.)"
    return render_template('index.html', message=message)

@app.route('/drop_all')
def drop_all():
    db.drop_all()
    message = "DB Dropped!!)"
    return render_template('index.html', message=message)

#Finally, this is for development purposes only. I normally have this in a
#file called RunServer.py. For actually delivering your application you should
#run behind a web server of some kind (Apache, Nginix, Heroku).

if __name__ == '__main__':
    db.create_all()
    create_example_data()
    app.run(debug=False)
