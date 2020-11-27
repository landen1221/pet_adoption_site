from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, BooleanField, IntegerField, RadioField, SelectField
from wtforms.validators import InputRequired, Email, Optional, URL, AnyOf, NumberRange

class AddPet(FlaskForm):
    """Form for adding a pet."""

    name = StringField("Pet name:*", validators=[InputRequired(message='Pet name required')])
    species = StringField("Species:*", validators=[InputRequired(message="Pet's species required"), AnyOf(['Dog', 'Cat', 'Porcupine'])])
    photo_url = StringField("Photo URL:", validators=[URL()])
    age = IntegerField("Pet's Age:", validators=[NumberRange(min=0, max=30)])
    notes = StringField("Additional Notes:")
    available = BooleanField("Is pet available?")