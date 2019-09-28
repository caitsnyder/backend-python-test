from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from alayatodo.models import User, Todo

# Authentication
class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Username"})
	password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
	submit = SubmitField('Sign in')

# Create post
class TodoForm(FlaskForm):
	description = StringField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description"})
	submit = SubmitField('Add')