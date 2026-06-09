import sqlite3

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from sigma_app.storage import create_user, verify_user


auth = Blueprint("auth", __name__)


def _database_path():
    return g.database_path


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username:
            flash("Informe um nome de usuario.", "error")
        elif not password:
            flash("Informe uma senha.", "error")
        elif len(password) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
        elif password != confirm_password:
            flash("As senhas nao conferem.", "error")
        else:
            try:
                user = create_user(_database_path(), username, password)
            except sqlite3.IntegrityError:
                flash("Esse nome de usuario ja existe.", "error")
            else:
                session["user_id"] = user["id"]
                flash("Cadastro realizado com sucesso.", "success")
                return redirect(url_for("main.index"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Informe usuario e senha.", "error")
        else:
            user = verify_user(_database_path(), username, password)
            if user is None:
                flash("Usuario ou senha invalidos.", "error")
            else:
                session["user_id"] = user["id"]
                flash("Login realizado com sucesso.", "success")
                return redirect(url_for("main.index"))

    return render_template("auth/login.html")


@auth.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    flash("Voce saiu do sistema.", "success")
    return redirect(url_for("main.index"))