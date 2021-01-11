from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField,SelectField
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

class AsignacionHabit(FlaskForm):
    fkIdHabitacion = StringField("Habitacion", validators=[DataRequired()])
    fkIdClientes = StringField("Cliente", validators=[DataRequired()])
    importeTotal = StringField("Importe Total", validators=[DataRequired()])
    numPersonas = StringField("Numero De Personas")
    diaInicio = StringField("Dia de Inicio", validators=[DataRequired()])
    diaFinalizado = StringField("Dia Finalizado", validators=[DataRequired()])
    diasDeEstancia = StringField("Dias de Estancia")

class CreacionUSR(FlaskForm):
    username = StringField("Nombre del Usuario",validators=[DataRequired()])
    password = PasswordField("Contraseña:",validators=[DataRequired()])
    submit = SubmitField("Crear")
    
class CreacionHabit(FlaskForm):
    numHabit = StringField("Numero de habitacion",validators=[DataRequired()])
    tipoHabit = SelectField("Tipo de habitacion", validators=[DataRequired()],choices=["","Individual", "Matrimonial", "QueenSize"])
    capXHabit = StringField("Capacidad de habitacion")
    costoXHabit = StringField("Costo de habitacion")
    submit = SubmitField("Crear")
