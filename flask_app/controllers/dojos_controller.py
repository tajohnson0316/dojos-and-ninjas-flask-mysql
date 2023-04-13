from flask import session, render_template, request, redirect
from flask_app import app
from flask_app.models.dojo_model import Dojo


@app.route("/")
def index():
    return redirect("/dojos")


@app.route("/dojos")
def get_dojos():
    list_of_dojos = Dojo.get_all()
    if len(list_of_dojos) == 0:
        return redirect("/dojos/form")
    return render_template("dojos.html", list_of_dojos=list_of_dojos)


@app.route("/dojos/new", methods=["POST"])
def create_dojo():
    dojo_id = Dojo.create_one({"name": request.form["name"]})
    return redirect("/dojos")


@app.route("/dojos/<int:id>/show")
def get_dojo_with_ninjas(id):
    dojo = Dojo.get_one_with_ninjas({"id": id})
    return render_template("display-dojo.html", dojo=dojo)
