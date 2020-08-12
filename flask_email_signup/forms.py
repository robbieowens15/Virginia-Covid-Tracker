from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from flask_email_signup.modles import Recipient

class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    #todo choices List will come from speadsheet
    location = SelectField('Locations', choices=['Fairfax County', 'Loudon County', 'Albemarle County'])
    submit = SubmitField('Subscribe')

    def validate_email(self, email):
        recipient = Recipient.query.filter_by(email=email.data).first()
        if recipient:
            raise ValidationError('This email address already is signed up')

class UnsubscribeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Unsubscribe')

    def validate_email(self, email):
        recipient = Recipient.query.filter_by(email=email.data).first()
        if not recipient:
            raise ValidationError('This email is not yet signed up')