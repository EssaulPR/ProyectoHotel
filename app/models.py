from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import login
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    type_User = db.Column(db.String(64))
    clientes = db.relationship("Cliente", backref="author", lazy="dynamic")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User {}>".format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Tabla de clientes
class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    nameClt = db.Column(db.String(50), index=True)    
    apellidoPateClt = db.Column(db.String(50), index=True)    
    apellidoMateClt = db.Column(db.String(50), index=True)
    phone = db.Column(db.String(12))
    phone2 = db.Column(db.String(12)) 
    placaCarro = db.Column(db.String(16))
    placaCarro2 = db.Column(db.String(16))
    activo = db.Column(db.Boolean, default=False)
    rentaHabitaciones = db.relationship("RentaHabitacion", backref="cliente", lazy="dynamic")
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return "<Cliente> {}".format(self.nameClt)
# Tabla de Habitaciones
class Habitacion(db.Model):
    __tablename__ = "habitaciones"
    id = db.Column(db.Integer, primary_key=True)
    numHabit = db.Column(db.Integer, index=True)
    tipoHabit = db.Column(db.String(25), index=True)
    capXHabit = db.Column(db.Integer)
    costoXHabit = db.Column(db.Integer)
    rentaHabitaciones = db.relationship("RentaHabitacion", backref="habitacion", lazy="dynamic")
    
    def toMap(self):
        diccionario = {}
        diccionario["Numero"]=self.numHabit
        diccionario["Tipo"]=self.tipoHabit        
        diccionario["Capacidad"]=self.capXHabit    
        diccionario["Costo"]=self.costoXHabit   
        return diccionario 


    def __repr__(self):
        return "<Habitacion> {}".format(self.numHabit)
# Tabla de RentaHabitaciones
class RentaHabitacion(db.Model):
    __tablename__ = "rentaHabitaciones"
    id = db.Column(db.Integer, primary_key=True)
    fkIdHabitacion = db.Column(db.Integer, db.ForeignKey("habitaciones.id"), index=True)
    fkIdClientes = db.Column(db.Integer, db.ForeignKey("clientes.id"), index=True)
    importeTotal = db.Column(db.Integer, index=True)
    numPersonas = db.Column(db.Integer, index=True)
    diaInicio = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    diaFinalizado = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    diasDeEstancia = db.Column(db.Integer)
    Apartado = db.Column(db.Boolean, default=False)
    Ocupado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<RentaHabitacion> {}".format(self.numPersonas)