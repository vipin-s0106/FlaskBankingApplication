from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length



class AddCards(FlaskForm):
    card_type1 = [('--Select--','--Select--'),('Credit Card','Credit Card'),('Debit Card','Debit Card')]
    card_holder_name = StringField('Card Holder Name',validators = [DataRequired(),Length(min = 2 , max = 30)])
    card_no = StringField('Card No',validators = [DataRequired(),Length(min = 2 , max = 16)])
    cvv = StringField('CVV',validators = [DataRequired(),Length(min = 3 , max = 3)])
    pin = PasswordField('PIN',validators = [DataRequired(),Length(min = 4 , max = 4)])
    card_type = SelectField('Card Type',validators=[DataRequired()],choices=card_type1)
    submit = SubmitField('Add Card')
 

    