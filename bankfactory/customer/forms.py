from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,FileField,IntegerField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileAllowed
from wtforms.fields.html5 import DateField



class RegistrationForm(FlaskForm):
    Country = [('India','India'),('America','America'),('UAE','UAE'),('England','England'),('Canada','Canada'),('China','China')]
    account_holder_name = StringField('Account Holder Name',validators = [DataRequired(),Length(min = 2 , max = 20)])
    account_number = StringField('Account Number',validators = [DataRequired(),Length(min = 2 , max = 16)])
    branch_name = StringField('Branch Name',validators = [DataRequired(),Length(min = 2 , max = 20)])
    ifsc = StringField('IFSC Code',validators = [DataRequired(),Length(min = 2 , max = 20)])
    mobile_no = StringField('Registered Mobile No',validators = [DataRequired(),Length(min = 8 , max = 10)])
    email = StringField('Registered Email',validators = [DataRequired(),Email()])
    dob = DateField('Date of Birth',validators = [DataRequired()])
    country = SelectField('Country',validators=[DataRequired()],choices=Country)
    submit = SubmitField('Sign Up')

    
class LoginForm(FlaskForm):
    customerid = StringField('Customer ID',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    submit = SubmitField('Login')
    
    
class SetPassword(FlaskForm):
    OTP = PasswordField('One Time Password',validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators = [DataRequired(),EqualTo('password')])
    submit = SubmitField('Save')
    
    
class ForgotPassword(FlaskForm):
    account_number = StringField('Account Number',validators = [DataRequired(),Length(min = 2 , max = 16)])
    email = StringField('Email',validators = [DataRequired(),Email()])
    submit = SubmitField('Send OTP') 
    

    