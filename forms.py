from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField, \
    SubmitField, RadioField, SelectField, DateTimeField, DecimalField, validators

class LandingPageForm(FlaskForm):
    age_group = SelectField("Age Group", choices = [], validators = [])

class MenuForm(FlaskForm):
    age_group = IntegerField("age_group",validators = [])
    selections = TextField("selections", validators = [])

class SummaryForm(FlaskForm):
    order = TextField("order", validators = [])


