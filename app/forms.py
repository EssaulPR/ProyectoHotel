from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired

class Login(FlaskForm):
    username = StringField("Usuario:",validators=[DataRequired()])
    password = PasswordField("Contraseña:",validators=[DataRequired()])
    remember_me = BooleanField("Recordar Usuario")
    submit = SubmitField("Iniciar")

class CreacionClt(FlaskForm):
    nameClt = StringField("Nombre: ", validators=[DataRequired()])
    apellidoPateClt = StringField("Apellido Paterno: ", validators=[DataRequired()])
    apellidoMateClt = StringField("Apellido Materno: ", validators=[DataRequired()])
    phone = StringField("Telefono: ")
    phone2 = StringField("Telefono auxiliar: ")
    placaCarro = StringField("Placa del carro: ")
    placaCarro2 = StringField("Segundo Carro: ")
    submit = SubmitField("Registrar")