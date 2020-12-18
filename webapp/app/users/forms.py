from wtforms import Form, StringField, PasswordField, validators, SelectField


class UserEditRegistrationForm(Form):
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')
    role = SelectField('Role', [validators.optional()], choices=[('admin', 'Admin'), ('user', 'User')])
    status = SelectField('Status', [validators.optional()], choices=[('active', 'Active'), ('inactive', 'Inactive')])
