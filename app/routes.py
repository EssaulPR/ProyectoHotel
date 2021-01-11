# Importamos de flask las librerias que son: v
from flask import render_template, flash, redirect, url_for
# Importamos la carpeta de app
from app import app, db
# Importamos de la carpeta app archivo forms la clase Login que es el formulario
from app.forms import Login,CreacionClt,AsignacionHabit,CreacionUSR,CreacionHabit
# Importamos el flask login que lo ocupamos con sus cosas
from flask_login import current_user, login_user,logout_user, login_required
# Importamos de la carpeta app archivo models la clase User que de la tabla de bdd
from app.models import User,Cliente,Habitacion,RentaHabitacion


# def LoginAdmin(current_user):
#     if current_user.type_User=="admin":
#         return redirect("/habit_admin")

# Para iniciar sesion en la app
@app.route("/", methods=["GET","POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("habit_UsR"))
    form = Login()
    if form.validate_on_submit():
        # Iniciar sesion con bdd
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Nombre de usuario o contraseña incorrecta.")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste session correctamente, Hola {}".format(form.username.data))
        #Para reconocer admin o recepcionista
        if user.type_User=="admin":
            return redirect("/habit_admin")
        return redirect("/habit_UsR")
    return render_template("login.html", form=form)

# Para desconectar usuarios
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# Habitaciones de con clientes recepcionista
@app.route("/habit_UsR")
@login_required
def habit_UsR():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    # Para verificar el usuario admin
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    # imprimir bdd rentaDeHabitaciones imprime todo de las 3 tablas renta,clientes y habitaciones
    subquery = db.session.query(RentaHabitacion, Cliente).join(Cliente.rentaHabitaciones).filter(RentaHabitacion.Ocupado == 1).subquery()
    habitaciones = db.session.query(Habitacion,subquery).outerjoin(subquery,Habitacion.id == subquery.c.fkIdHabitacion).all()
    return render_template("habit_UsR.html", habitaciones = habitaciones)  

# Asignacion de habitaciones
@app.route("/asignacion_habit/add/<int:id>", methods=["GET","POST"])
@login_required
def asignacion_habit():
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
        #Metodos de la bdd con el formulario DETALLES QUE NO SE COMO SOLUCIONAR
        subquery = db.session.query(RentaHabitacion, Cliente).join(Cliente.rentaHabitaciones).filter(RentaHabitacion.Ocupado == 1).subquery()
        habitaciones = db.session.query(Habitacion,subquery).outerjoin(subquery,Habitacion.id == subquery.c.fkIdHabitacion).all()
        
        rent = RentaHabitacion.query.filter_by(id=id).first()
        if rent:
            form = AsignacionHabit()
            if form.validate_on_submit():
                rent.fkIdHabitacion = form.fkIdHabitacion.data
                rent.fkIdClientes = form.fkIdClientes.data
                rent.importeTotal = form.importeTotal.data
                rent.numPersonas = form.numPersonas.data
                rent.diaInicio = form.diaInicio.data
                rent.diaFinalizado = form.diaFinalizado.data
                rent.diasDeEstancia = form.diasDeEstancia.data
                db.session.add(rent)
                db.session.commit()
                return redirect(url_for("habit_UsR"))
            form.fkIdHabitacion.data =  rent.fkIdHabitacion
            form.fkIdClientes.data = rent.fkIdClientes
            form.importeTotal.data = rent.importeTotal
            form.numPersonas.data = rent.numPersonas
            form.diaInicio.data = rent.diaInicio
            form.diaFinalizado.data = rent.diaFinalizado
            form.diasDeEstancia.data = rent.diasDeEstancia
            return render_template("asignacion_habit.html", form=form, add=True)
        else:
            flash("No existe")
        return redirect(url_for("habit_UsR"))

# Descoupar habitacion Recepcionista
@app.route("/update_Habit_desocupada/update<int:id>", methods=["GET","POST"])
@login_required
def update_Habit_desocupada(id):
    rent = RentaHabitacion.query.filter_by(id=id).first()
    clt = Cliente.query.filter_by(id=id).first()
    clt.activo = 0
    rent.Ocupado = 0
    db.session.add(rent,clt)
    db.session.commit()
    return redirect(url_for("habit_UsR" ,update=True))
 
# Mostrar clientes en recepcionista
@app.route("/client_UsR")
@login_required
def client_UsR():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    # imprimir lo que mando desde crearClt
    clientes = Cliente.query.all()
    return render_template("client_UsR.html", clientes = clientes) 

# Crear clientes en recepcionista
@app.route("/crearClt", methods=["GET","POST"])
@login_required
def crearClt():
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    form = CreacionClt()
    if form.validate_on_submit():
        #Metodos de la bdd con el formulario
        clt = Cliente()
        clt.nameClt = form.nameClt.data
        clt.apellidoPateClt = form.apellidoPateClt.data
        clt.apellidoMateClt = form.apellidoMateClt.data
        clt.phone = form.phone.data
        clt.phone2 = form.phone2.data
        clt.placaCarro = form.placaCarro.data
        clt.placaCarro2 = form.placaCarro2.data
        # clt.users_id = current_user.id
        db.session.add(clt)
        db.session.commit()
        return redirect(url_for("client_UsR"))
    return render_template("crearClt.html", form=form)

# Editar clientes de recepcionista
@app.route("/crearCltEdit/edit/<int:id>", methods=["POST"])
@login_required
def edit_crearClt(id):
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    clt = Cliente.query.filter_by(id=id).first()
    if clt:
        form = CreacionClt()
        if form.validate_on_submit():
            clt.nameClt = form.nameClt.data
            clt.apellidoPateClt = form.apellidoPateClt.data
            clt.apellidoMateClt = form.apellidoMateClt.data  
            clt.phone = form.phone.data  
            clt.phone2 = form.phone2.data
            clt.placaCarro = form.placaCarro.data
            clt.placaCarro2 = form.placaCarro2.data
            db.session.add(clt)
            db.session.commit()
            return redirect(url_for("client_UsR"))
        form.nameClt.data = clt.nameClt
        form.apellidoPateClt.data = clt.apellidoPateClt
        form.apellidoMateClt.data = clt.apellidoMateClt
        form.phone.data = clt.phone
        form.phone2.data = clt.phone2
        form.placaCarro.data = clt.placaCarro 
        form.placaCarro2.data = clt.placaCarro2 
        return render_template("crearCltEdit.html", form=form, edit=True)
    else:
        flash("No existe")
    return redirect(url_for("client_UsR")) 

# Habitaciones de admin
@app.route("/habit_admin")
@login_required
def habit_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    # Por ahorita solo se muestran habitaciones! se requiere cambiar el query .filter_by(numHabit="1")
    habitaciones = Habitacion.query.all()
    return render_template("habit_admin.html", habitaciones = habitaciones)

# Habitaciones con clientes de admin
@app.route("/habit_asig_admin")
@login_required
def habit_asig_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    subquery = db.session.query(RentaHabitacion, Cliente).join(Cliente.rentaHabitaciones).filter(RentaHabitacion.Ocupado == 1).subquery()
    habitaciones = db.session.query(Habitacion,subquery).outerjoin(subquery,Habitacion.id == subquery.c.fkIdHabitacion).all()
    return render_template("habit_asig_admin.html", habitaciones = habitaciones)

# Desocupar habitacion admin
@app.route("/update_Habit_desocupada_admin/update<int:id>", methods=["GET","POST"])
@login_required
def update_Habit_desocupada_admin(id):
    rent = RentaHabitacion.query.filter_by(id=id).first()
    clt = Cliente.query.filter_by(id=id).first()
    clt.activo = 0
    rent.Ocupado = 0
    db.session.add(rent,clt)
    db.session.commit()
    return redirect(url_for("habit_asig_admin" ,update=True))


# Crear Habitacion Admin
@app.route("/crear_habit", methods=["GET","POST"])
@login_required
def crear_habit():
    form = CreacionHabit()
    if form.validate_on_submit():
        #Metodos de la bdd con el formulario
        habit = Habitacion()
        habit.numHabit = form.numHabit.data
        habit.tipoHabit = form.tipoHabit.data
        habit.capXHabit = form.capXHabit.data
        habit.costoXHabit = form.costoXHabit.data
        db.session.add(habit)
        db.session.commit()
        return redirect(url_for("habit_admin"))
    return render_template("crear_habit.html", form=form)

# Edit Habitacion Admin
@app.route("/Edit_Habit/edit/<int:id>", methods=["GET","POST"])
@login_required
def Edit_Habit(id):
    h = Habitacion.query.filter_by(id=id).first()
    if h:
        form = CreacionHabit()
        if form.validate_on_submit():
            h.numHabit = form.numHabit.data
            h.tipoHabit = form.tipoHabit.data
            h.capXHabit = form.capXHabit.data  
            h.costoXHabit = form.costoXHabit.data  
            db.session.add(h)
            db.session.commit()
            return redirect(url_for("habit_admin"))
        form.numHabit.data = h.numHabit
        form.tipoHabit.data = h.tipoHabit
        form.capXHabit.data = h.capXHabit
        form.costoXHabit.data  = h.costoXHabit
        return render_template("Edit_Habit.html", form=form, edit=True)
    else:
        flash("No existe")
    return redirect(url_for("habit_admin"))

# Eliminar Habitacion Admin
@app.route("/Delete_Habit/delete/<int:id>", methods=["GET","POST"])
@login_required
def Delete_Habit(id):
    h = Habitacion.query.filter_by(id=id).first()
    if h:
        db.session.delete(h)
        db.session.commit()
        return redirect(url_for("habit_admin",delete=True))
    else:
        flash("No existe")
    return redirect(url_for("habit_admin"))


# Clientes de admin
@app.route("/client_admin")
@login_required
def client_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    # imprimir lo que mando desde crearClt
    clientes = Cliente.query.all()
    return render_template("client_admin.html", clientes = clientes)

# crear clientes admin
@app.route("/crear_Clt_Admin", methods=["GET","POST"])
@login_required
def crear_Clt_Admin():
    form = CreacionClt()
    if form.validate_on_submit():
        #Metodos de la bdd con el formulario
        clt = Cliente()
        clt.nameClt = form.nameClt.data
        clt.apellidoPateClt = form.apellidoPateClt.data
        clt.apellidoMateClt = form.apellidoMateClt.data
        clt.phone = form.phone.data
        clt.phone2 = form.phone2.data
        clt.placaCarro = form.placaCarro.data
        clt.placaCarro2 = form.placaCarro2.data
        clt.users_id = current_user.id
        db.session.add(clt)
        db.session.commit()
        return redirect(url_for("client_admin"))
    return render_template("crear_Clt_Admin.html", form=form)

# editar clientes admin
@app.route("/crear_Clt_AdminEdit/edit/<int:id>", methods=["POST"])
@login_required
def crear_Clt_AdminEdit(id):
    clt = Cliente.query.filter_by(id=id).first()
    if clt:
        if current_user.id == clt.users_id:
            pass
            # Editar
            form = CreacionClt()
            if form.validate_on_submit():
                clt.nameClt = form.nameClt.data
                clt.apellidoPateClt = form.apellidoPateClt.data
                clt.apellidoMateClt = form.apellidoMateClt.data  
                clt.phone = form.phone.data  
                clt.phone2 = form.phone2.data
                clt.placaCarro = form.placaCarro.data
                clt.placaCarro2 = form.placaCarro2.data
                db.session.add(clt)
                db.session.commit()
                return redirect(url_for("client_admin"))
            form.nameClt.data = clt.nameClt
            form.apellidoPateClt.data = clt.apellidoPateClt
            form.apellidoMateClt.data = clt.apellidoMateClt
            form.phone.data = clt.phone
            form.phone2.data = clt.phone2
            form.placaCarro.data = clt.placaCarro 
            form.placaCarro2.data = clt.placaCarro2 
            return render_template("crear_Clt_AdminEdit.html", form=form, edit=True)
        else:
            flash("No tienes permisos para borrar este contacto")
    else:
        flash("No existe")
    return redirect(url_for("client_admin"))
# Eliminar clientes admin
@app.route("/Delete_cliente/delete/<int:id>", methods=["GET","POST"])
@login_required
def Delete_cliente(id):
    c = Cliente.query.filter_by(id=id).first()
    if c:
        db.session.delete(c)
        db.session.commit()
        return redirect(url_for("client_admin",delete=True))
    else:
        flash("No existe")
    return redirect(url_for("client_admin"))

#Usuarios de admin
@app.route("/usuario_admin")
@login_required
def usuario_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    # Me trae todo
    # usuarios = User.query.all()
    # Me trae todo lo que sea solamente recepcionista
    usuarios = User.query.filter_by(type_User="recepcionista").all()
    return render_template("usuario_admin.html",usuarios = usuarios ) 

# Crear USR Admin
@app.route("/crear_USR", methods=["GET","POST"])
@login_required
def crear_USR():
    form = CreacionUSR()
    if form.validate_on_submit():
        #Metodos de la bdd con el formulario
        u = User()
        u.username = form.username.data
        u.set_password (form.password.data)
        u.type_User = ("recepcionista")
        db.session.add(u)
        db.session.commit()
        return redirect(url_for("usuario_admin"))
    return render_template("crear_USR.html", form=form) 

# Eliminar usuarios admin
@app.route("/Delete_usuarios/delete/<int:id>", methods=["GET","POST"])
@login_required
def Delete_usuarios(id):
    u = User.query.filter_by(id=id).first()
    if u:
        db.session.delete(u)
        db.session.commit()
        return redirect(url_for("usuario_admin",delete=True))
    else:
        flash("No existe")
    return redirect(url_for("usuario_admin"))












# No se usa por el momento!
# @app.route("/habit_UsR/api")
# def habit_UsR_api():
#     # imprimir bdd habitaciones
#     habitaciones = Habitacion.query.all()
#     json = {}
#     lista = []
#     for habitacion in habitaciones:
#         lista.append(habitacion.toMap())
#     json["Habitaciones"]= lista
#     return json  