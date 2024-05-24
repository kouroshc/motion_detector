from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class TimeFrame_Form(FlaskForm):
    time = SelectField('بازه زمانی',
                           choices=[('1', 'همزمان'), ('0.1', '0.1'), ('0.5', '0.5'), ('1', '1'), ('2', '2'),
                                    ('5', '5'), ('10', '10')], validators=[DataRequired()])
    submit = SubmitField('ثبت')