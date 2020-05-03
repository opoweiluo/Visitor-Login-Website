from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length, Email, ValidationError
from wtforms.fields.html5 import EmailField
import phonenumbers

class FormRegister(Form):

    username = StringField('Your Name', validators=[
        InputRequired(),
        Length(1, 30, message='name must be between 1 and 30 characters')
    ])
    email = EmailField('Email', validators=[
        InputRequired(),
        Length(1, 50, message='email must be between 1 and 50 characters'),
        Email()
    ])
    phone = StringField('US Phone Number', validators=[
        InputRequired()
    ])
    hostname = StringField('Person You Are Visiting', validators=[
        InputRequired(),
        Length(1, 30, message='name must be between 1 and 30 characters')
    ])
    submit = SubmitField('Register New Visitor')

    def validate_phone(self, phone):
        if len(phone.data) > 16 or len(phone.data) < 10:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1" + phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
