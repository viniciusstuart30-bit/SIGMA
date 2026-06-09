import sqlite3

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from sigma_app.storage import create_leader, verify_leader


auth = Blueprint("auth", __name__)


def _database_path():
    return g.database_path


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        leader_name = request.form.get("leader_name", "").strip()
        sector = request.form.get("sector", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not leader_name:
            flash("Informe o nome do lider.", "error")
        elif not sector:
            flash("Informe o setor.", "error")
        elif not password:
            flash("Informe uma senha.", "error")
        elif len(password) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
        elif password != confirm_password:
            flash("As senhas nao conferem.", "error")
        else:
            try:
                leader = create_leader(_database_path(), leader_name, sector, password)
            except sqlite3.IntegrityError:
                flash("Ja existe um lider cadastrado com este nome e setor.", "error")
            else:
                session["leader_id"] = leader["id"]
                flash("Cadastro realizado com sucesso.", "success")
                return redirect(url_for("main.index"))

    return render_template("auth/register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        leader_name = request.form.get("leader_name", "").strip()
        password = request.form.get("password", "")

        if not leader_name or not password:
            flash("Informe nome do lider e senha.", "error")
        else:
            leader = verify_leader(_database_path(), leader_name, password)
            if leader is None:
                flash("Dados invalidos.", "error")
            else:
                session["leader_id"] = leader["id"]
                flash("Login realizado com sucesso.", "success")
                return redirect(url_for("main.index"))

    return render_template("auth/login.html")


@auth.route("/logout", methods=["POST"])
def logout():
    session.pop("leader_id", None)
    flash("Voce saiu do sistema.", "success")
    return redirect(url_for("main.index"))