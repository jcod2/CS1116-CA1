from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import InputRequired, EqualTo, Length 

class RegistrationForm(FlaskForm):
    user_id = StringField("Username: ", 
        validators=[InputRequired(), Length(min=3, message="Username must be at least 3 characters.")])
    password = PasswordField("Password: ", 
        validators=[InputRequired(message="Password required."), Length(min=5, message="Password must be at least 5 characters.")])
    confirm_password = PasswordField("Confirm Password: ", 
        validators=[InputRequired(message="Password required."), EqualTo("password", message="Passowrds did not match.")])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    user_id = StringField("Username: ", 
        validators=[InputRequired(message="Username required."), Length(min=3, message="Userame must be at least 3 characters.")])
    password = PasswordField("Password: ", 
        validators=[InputRequired(message="Password required.")])
    submit = SubmitField("Login")

class AdminForm(FlaskForm):
    options = SelectField("Add or Remove user", 
        choices=["Add user", "Delete user","Show all users", "Reset users"])
    submit = SubmitField("Submit")
    
class AdminAddForm(FlaskForm):
    user_id = StringField("Username: ", 
        validators=[InputRequired(message="Username required."), Length(min=3, message="Userame must be at least 3 characters.")])
    password = PasswordField("User Password: ", 
        validators=[InputRequired(message="Password required."), Length(min=5, message="Password must be at least 5 characters.")])
    confirm_password = PasswordField("Confirm User Password: ", 
        validators=[InputRequired(message="Password required."), EqualTo("password", message="Passowrds did not match.")])
    submit = SubmitField("Create User")

class AdminDelForm(FlaskForm):
    user_id = StringField("Username: ", 
        validators=[InputRequired(message="Username required"), Length(min=3, message="Userame must be at least 3 characters.")])
    password = PasswordField("Admin Password: ", 
        validators=[InputRequired(message="Password required.")])
    confirm_password = PasswordField("Confirm Admin Password: ", 
        validators=[InputRequired(message="Password required."), EqualTo("password", message="Passowrds did not match.")])
    submit = SubmitField("Delete User")

# class NavForm(FlaskForm):
#     prev = SubmitField("PREV", default="PREV")
#     next = SubmitField("NEXT", default="NEXT")

# class DexForm(FlaskForm):
#     index = StringField("Go to (ID):")

class PokedexForm(FlaskForm):
    name = StringField("Name: ", 
        render_kw={"placeholder": "e.g. Charmander"})
    nat_dex = StringField("National Dex #:")
    prim_type = SelectField("Primary Type:")
    sec_type = SelectField("Secondary Type:")
    classification = SelectField("Classification:")
    hidden_ab = SelectField("Hidden Ability:")
    alt_form = SelectField("Alternate Form:")
    leg_type = SelectField("Legendary Type:")
    region = SelectField("Region of Origin:")
    stats = BooleanField("Show Stat's?")
    evs = BooleanField("Show EV's?")
    misc = BooleanField("Show Misc Data?")
    submit = SubmitField("Search")
