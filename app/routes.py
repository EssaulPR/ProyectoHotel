# Importamos de flask las librerias que son: v
from flask import render_template, flash, redirect, url_for
# Importamos la carpeta de app
from app import app, db
# Importamos de la carpeta app archivo forms la clase Login que es el formulario
from app.forms import Login,CreacionClt
# Importamos el flask login que lo ocupamos con sus cosas
from flask_login import current_user, login_user,logout_user, login_required
# Importamos de la carpeta app archivo models la clase User que de la tabla de bdd
from app.models import User,Cliente,Habitacion,RentaHabitacion


# def LoginAdmin(current_user):
#     if current_user.type_User=="admin":
#         return redirect("/habit_admin")

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

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/habit_UsR")
@login_required
def habit_UsR():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    # Agregar esto a todas las rutas
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    # imprimir bdd habitaciones
    habitaciones = Habitacion.query.all()
    return render_template("habit_UsR.html", habitaciones = habitaciones)  

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

@app.route("/crearClt", methods=["GET","POST"])
@login_required
def crearClt():
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    form = CreacionClt()
    if form.validate_on_submit():
        # Metemos datos a la bdd
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
        return redirect(url_for("client_UsR"))
    return render_template("crearClt.html", form=form)

# Se crea una ruta para editar con metodo post
@app.route("/crearCltEdit/edit/<int:id>", methods=["POST"])
@login_required
def edit_crearClt(id):
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
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
            flash("No tienes permisos para borrar este contacto")
    else:
        flash("No existe")
    return redirect(url_for("client_UsR"))
# Asignacion de habitaciones
@app.route("/asignacion_habit")
@login_required
def asignacion_habit():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    if current_user.type_User=="admin":
        return redirect("/habit_admin")
    return render_template("asignacion_habit.html") 

# Admin
@app.route("/habit_admin")
@login_required
def habit_admin():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("habit_admin.html") 