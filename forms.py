from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    """form to register as a User"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)])
    email = StringField("Email", validators=[InputRequired(),Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """form for User to login"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=30)])


class FeedbackForm(FlaskForm):
    """form for user to write feedback"""

    title = StringField("Title", validators=[InputRequired(), Length(max=50)])
    content = StringField("Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""