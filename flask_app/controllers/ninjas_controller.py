from flask import session, render_template, request, redirect
from flask_app import app
from flask_app.models.dojo_model import Dojo
from flask_app.models.dojo_model import Ninja


@app.route("/ninja/form", methods=["GET"])
def display_ninja_form():
    list_of_dojos = Dojo.get_all()
    return render_template("new-ninja-form.html", list_of_dojos=list_of_dojos)


@app.route("/ninja/new", methods=["POST"])
def create_ninja():
    new_ninja = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "age": request.form["age"],
        "dojo_id": request.form["location"],
    }

    created_ninja = Ninja.create_one(new_ninja)

    # incorrect form values
    if created_ninja == False:
        return redirect("/ninja/form")

    return redirect("/dojos")
