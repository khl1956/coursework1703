from flask_wtf import FlaskForm
from wtforms import SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length

class HeartForm(FlaskForm):

    heart_id = IntegerField('id', validators=[DataRequired("Please enter heart_id.")])

    age = IntegerField('age', validators=[DataRequired("Please enter your age."), NumberRange(min=18, max=100)])

    sex = SelectField('sex',choices=[('male','male'), ('female','female')], validators=[DataRequired("Please enter your age.")])

    trestbps = FloatField('resting blood pressure (in mm Hg on admission to the hospital)', validators=[DataRequired('Please enter your'), NumberRange(min=80, max=250)])

    chol = FloatField('serum cholestoral in mg/dl', validators=[DataRequired(), NumberRange(min=0, max=1000)])

    thalach = IntegerField('maximum heart rate achieved', validators=[DataRequired(), NumberRange(min=10, max=250)])

    submit = SubmitField("Save")

