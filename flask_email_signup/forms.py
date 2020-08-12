from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email
from flask_email_signup.modles import Recipient
 

class SubscribeForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    choices = ['Accomack','Albemarle','Alleghany','Amelia','Amherst','Appomattox','Arlington','Augusta',
    'Bath','Bedford','Bland','Botetourt','Brunswick','Buchanan','Buckingham', 'Campbell',
    'Caroline','Carroll','Charles City','Charlotte','Chesterfield','Clarke','Craig','Culpeper',
    'Cumberland','Dickenson','Dinwiddie','Essex','Fairfax','Fauquier','Floyd','Fluvanna',
    'Franklin County','Frederick','Giles','Gloucester','Goochland','Grayson','Greene',
    'Greensville','Halifax','Hanover','Henrico','Henry','Highland','Isle of Wight','James City',
    'King and Queen','King George','King William','Lancaster','Lee','Loudoun','Louisa','Lunenburg',
    'Madison','Mathews','Mecklenburg','Middlesex','Montgomery','Nelson','New Kent','Northampton',
    'Northumberland','Nottoway','Orange','Page','Patrick','Pittsylvania','Powhatan','Prince Edward',
    'Prince George','Prince William','Pulaski','Rappahannock','Richmond County','Roanoke County',
    'Rockbridge','Rockingham','Russell','Scott','Shenandoah','Smyth','Southampton','Spotsylvania',
    'Stafford','Surry','Sussex','Tazewell','Warren','Washington','Westmoreland','Wise','Wythe','York',
    'Alexandria','Bristol','Buena Vista City','Charlottesville','Chesapeake','Colonial Heights',
    'Covington','Danville','Emporia','Fairfax City','Falls Church','Franklin City','Fredericksburg',
    'Galax','Hampton','Harrisonburg','Hopewell','Lexington','Lynchburg','Manassas City','Manassas Park',
    'Martinsville','Newport News','Norfolk','Norton','Petersburg','Poquoson','Portsmouth','Radford',
    'Richmond City','Roanoke City','Salem','Staunton','Suffolk','Virginia Beach','Waynesboro','Williamsburg',
    'Winchester']
    choices.sort()
    location = SelectField('Locations', choices=choices)
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