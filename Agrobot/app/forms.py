from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Is Admin')
    submit = SubmitField('Register')

class DiseaseForm(FlaskForm):
    name = StringField('Disease Name (English)', validators=[DataRequired()])
    image_class_name = StringField('Image Class Name')  # Optional
    symptom_en = TextAreaField('Symptom (English)', validators=[DataRequired()])
    symptom_hi = TextAreaField('Symptom (हिन्दी)')
    symptom_bn = TextAreaField('Symptom (বাংলা)')
    symptom_te = TextAreaField('Symptom (తెలుగు)')
    prevention_en = TextAreaField('Prevention/Treatment (English)', validators=[DataRequired()])
    prevention_hi = TextAreaField('Prevention/Treatment (हिन्दी)')
    prevention_bn = TextAreaField('Prevention/Treatment (বাংলা)')
    prevention_te = TextAreaField('Prevention/Treatment (తెలుగు)')
    submit = SubmitField('Submit')

class ChatForm(FlaskForm):
    language = SelectField('Preferred Language', choices=[('en', 'English'), ('hi', 'हिन्दी'), ('bn', 'বাংলা'), ('te', 'తెలుగు')], validators=[DataRequired()])
    symptom = TextAreaField('Plant Symptom')
    image = FileField('Upload Plant Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
    submit = SubmitField('Submit')