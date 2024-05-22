from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from utils.decorators import role_required
from views import user_view
from views import patient_view
from models.user_model import User


user_bp = Blueprint("user", __name__)

@user_bp.route("/")
def index():
   return redirect(url_for("user.login"))


@user_bp.route("/users", methods=["GET", "POST"])
#@role_required("admin")
def create_user():
   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]
      role = request.form["role"]
      existing_user = User.query.filter_by(username=username).first()
      if existing_user:
         flash("El nombre de usuario ya está en uso", "error")
         return redirect(url_for("user.create_user"))
      user = User(username, password, role=role)
      user.set_password(password)
      user.save()
      flash("Usuario registrado exitosamente", "success")
      return redirect(url_for("user.login"))
   return user_view.register()


@user_bp.route("/login", methods=["GET", "POST"])
def login():
   if request.method == "POST":
      username = request.form["username"]
      password = request.form["password"]
      user = User.get_user_by_username(username)
      if user and check_password_hash(user.password_hash, password):
         login_user(user)
         flash("Inicio de sesión exitoso", "success")
      else:
         flash("Nombre de Usuario o Contraseña Incorrectos", "error")
      return redirect(url_for("patient.list_patients"))
   return user_view.login()


@user_bp.route("/logout")
@login_required
def logout():
   logout_user()
   flash("Sesión cerrada exitosamente", "success")
   return redirect(url_for("user.login"))
