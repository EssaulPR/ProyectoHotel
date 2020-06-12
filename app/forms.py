from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    username = StringField("Usuario:",validators=[DataRequired()])
    password = PasswordField("Contraseña:",validators=[DataRequired()])
    remember_me = BooleanField("Recordar Usuario")
    submit = SubmitField("Iniciar")