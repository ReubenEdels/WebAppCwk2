from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.widgets import TextArea

class NewReview(FlaskForm):
    game = SelectField('Game', choices=[], validators=[DataRequired()])
    rating = RadioField('Rating', choices=[1,2,3,4,5,6,7,8,9,10], validators=[DataRequired()])
    review = TextAreaField('Review', validators=[Length(max=100)])


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=8,max=15)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8,max=15)])
    submit = SubmitField('Login')