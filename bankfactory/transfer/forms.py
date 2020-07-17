from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField,RadioField,IntegerField,FloatField
from wtforms.validators import DataRequired,Email,Length



class AddPayee(FlaskForm):
    register_for1 = [('Axis Bank Accounts','Axis Bank Accounts'),('Other Axis Bank Accounts','Other Axis Bank Accounts')]
    payee_name = StringField('Payee Name',validators = [DataRequired(),Length(min = 2 , max = 20)])
    register_for = SelectField('Register Payee For',validators=[DataRequired()],choices=register_for1)
    payee_account_number = StringField('Payee Account Number',validators = [DataRequired(),Length(min = 2 , max = 16)])
    payee_email = StringField('Payee Email ID',validators = [DataRequired(),Email()])
    payee_bank_name = StringField('Payee Bank Name',validators = [DataRequired(),Length(min = 8 , max = 20)])
    payee_branch_name = StringField('Payee Branch Name',validators = [DataRequired(),Length(min = 2 , max = 20)])
    payee_ifsc = StringField('IFSC Code',validators = [DataRequired(),Length(min = 2 , max = 20)])
    submit = SubmitField('Add Payee')

    
class BeginPayment(FlaskForm):
    payement_type = RadioField('Payement Type',validators=[DataRequired()],choices=[('NEFT','NEFT'),('RTGS','RTGS'),('IMPS 24*7','IMPS 24*7')])
    amount = FloatField('Amount',validators = [DataRequired()])
    remarks = StringField('Remarks')
    submit = SubmitField('Pay')
    
    