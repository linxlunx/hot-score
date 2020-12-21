from wtforms import StringField, PasswordField, validators, Form


class LoginForm(Form):
    username = StringField('Username', [validators.DataRequired()], render_kw={'placeholder': 'Username'})
    password = PasswordField('Password', [validators.DataRequired()], render_kw={'placeholder': 'Password'})
