from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length


class EditDiseaseForm(FlaskForm):
    disease_name = StringField('name', validators=[DataRequired(), Length(2)])
    severity = IntegerField('severity', validators=[DataRequired(), NumberRange(min=1, max=10)])

    submit = SubmitField("Save")