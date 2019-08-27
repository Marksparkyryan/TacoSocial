from flask import Flask, redirect, url_for, render_template, flash

import forms
import models
from secret import key as secretkey

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = secretkey


@app.route("/register", methods=["GET","POST"])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        flash("Yay! You registered!", "success")
        new_user = models.User.create(
            email=form.email.data,
            password=form.password.data,
        )
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login")
def login():
    return "login page!"



if __name__ == "__main__":
    models.initialize_database()
    app.run(debug=DEBUG, host=HOST, port=PORT)



