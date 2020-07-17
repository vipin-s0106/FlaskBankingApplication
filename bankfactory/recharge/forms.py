from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,FileField,IntegerField,SelectField,FloatField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileAllowed
from wtforms.fields.html5 import DateField



class MobileRecharge(FlaskForm):
    #Mobile Plan
    mobileno = IntegerField('Mobile No',validators=[DataRequired()])
    Mobile_Plan = [('11 ₹      8-days validity','11₹      8-days validity'),('49 ₹      21-days validity','49₹      21-days validity'),('149 ₹      1-month validity','149₹      1-month validity')]
    mobileplan = SelectField('Mobile Plan',validators=[DataRequired()],choices=Mobile_Plan)
    Provider = [('Airtel','Airtel'),('Vodafone','Vodafone'),('Idea','Idea'),('Jio','Jio'),('BSNL','BSNL')]
    provider = SelectField('Provider',validators=[DataRequired()],choices=Provider)
    submit = SubmitField('Recahrge')
     
    
class DTHRecharge(FlaskForm):
    #DTH
    consumerno = StringField('Consumer No',validators=[DataRequired()])
    DTH_Plan = [('300 ₹     30-days validity','300₹     30-days validity'),('500 ₹  59-days validity','500₹  59-days validity'),('1000 ₹  6-month validity','1000 ₹  6-month validity')]
    dthplan = SelectField('DTH Plan',validators=[DataRequired()],choices=DTH_Plan)
    DTH_Provider = [('Airtel','Airtel'),('TataSky','TataSky'),('DishTv','DishTv'),('Jio','Jio')]
    dthprovider = SelectField('Provider',validators=[DataRequired()],choices=DTH_Provider)
    submit = SubmitField('Pay')
    
class ElecRecharge(FlaskForm):
   #Electricity
    consumerno = StringField('Consumer No',validators=[DataRequired()])
    Elecprovider = [('Mahavitran','Mahavitran'),('Reliance','Reliance'),('Adani','Adani')]
    provider = SelectField('Electricity Provider',validators=[DataRequired()],choices=Elecprovider)
    amount = FloatField('Bill Amount',validators=[DataRequired()])
    submit = SubmitField('Pay')
    
    
