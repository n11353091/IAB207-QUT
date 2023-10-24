from flask_wtf import FlaskForm
from wtforms import DateField, IntegerField, SelectField, TimeField
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new event
class EventForm(FlaskForm):
    status = SelectField('Status', choices=[('open', 'Open'), ('closed', 'Closed'), ('sold out', 'Sold out')], default='Open')
    name = StringField('What is the name of the event?', validators=[InputRequired()])
    type = SelectField(
        'What is your employment type?',
        coerce=str,
        default='',
        choices=(
            ('Business', 'Business'),
            ('Career', 'Career'),
            ('Networking', 'Networking'),
            ('Health', 'Health'),
            ('Education', 'Education'),
            ('Sales', 'Sales'),
            ('Marketing', 'Marketing'),
            ('Tradeshows', 'Tradeshows'),
        )
    )
    event_date = DateField('What is the date of the event?', validators=[InputRequired()])
    start_time = TimeField('What is the start time of the event?', validators=[InputRequired()])
    end_time = TimeField('What is the finish time of the event?', validators=[InputRequired()])
    location = StringField('What is the location of your event?', validators=[InputRequired()])
    description = TextAreaField("Add a description of what value your event will provide for it's attendees:", validators=[InputRequired()])
    expire_date = DateField('When would you like your event to expire?', validators=[InputRequired()])
    image = FileField('Add a picture of what your event will look like:', validators=[
        FileRequired(message='Image cannot be empty'),
        FileAllowed(ALLOWED_FILE, message='Only supports png,jpg,JPG,PNG')])

    submit = SubmitField("Create")


#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #phone number
    contact_number=StringField("Contact number", validators=[InputRequired()])
    #address
    address=StringField("Your home address", validators=[InputRequired()])
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', validators=[InputRequired()])
  submit = SubmitField('Create')

class OrderForm(FlaskForm):
    ticket_type = SelectField(
        'What is your employment type?',
        coerce=str,
        default='',
        choices=(
           ('Observer', 'Observer'),
           ('Participant', 'Participant')
        )
    )
    ticket_number = IntegerField(
        'How many tickets would you like to purchase?',
        validators=[InputRequired(), NumberRange(min=1, max=99, message='Please enter a valid number of tickets')]
    )
    submit = SubmitField('Book')
  
   
   