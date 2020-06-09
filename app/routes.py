# Importamos de flask las librerias que son: v
from flask import render_template, flash, redirect, url_for
# Importamos la carpeta de app
from app import app
# Importamos de la carpeta app archivo forms la clase Login que es el formulario
from app.forms import Login
# Importamos el flask login que lo ocupamos con sus cosas
from flask_login import current_user, login_user,logout_user, login_required
# Importamos de la carpeta app archivo models la clase User que de la tabla de bdd
from app.models import User
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
            flash("No se encontro el usuario o la contraseña esta incorrecta.")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste session correctamente, Hola {}".format(form.username.data))
        return redirect("/habit_UsR")
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

# @app.route("/usuarioR")
# @login_required
# def usuarioR():
#     return render_template("usuarioR.html")

@app.route("/habit_UsR")
@login_required
def habit_UsR():
    return render_template("habit_UsR.html")    

@app.route("/client_UsR")
@login_required
def client_UsR():
    return render_template("client_UsR.html")       