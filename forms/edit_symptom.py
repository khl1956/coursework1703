from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length


class EditSymptomForm(FlaskForm):


    description = StringField('description', validators=[DataRequired(), Length(5)])

    submit = SubmitField("Save")
