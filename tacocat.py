import datetime
from flask import Flask, redirect, url_for, render_template, flash, g, request
from flask_bcrypt import check_password_hash
from flask_login import (login_user, LoginManager, current_user, login_required,
                        logout_user)

import forms
import models
from secret import key as secretkey

DEBUG = True
PORT = 8000
HOST = "0.0.0.0"

app = Flask(__name__)
app.secret_key = secretkey

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    try:
        g.db = models.DATABASE
        g.db.connect()
    except models.OperationalError:
        pass
    finally:
        g.user = current_user
        g.now = datetime.datetime.now()


@app.after_request
def after_request(response):
    """Close the database connection after each request"""
    g.db.close()
    # below is for testing
    #print(response.status)
    #print(response.headers)
    #print(response.location)
    #print(response.get_data(as_text=True))
    #print("***************")
    return response


@app.route("/register", methods=["GET","POST"])
def registration():
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        try:
            new_user = models.User.create_user(
                email=form.email.data,
                password=form.password.data,
            )
        except ValueError:
            pass
        else:
            flash("Yay! You registered!", "success")
            return redirect(url_for("index"))     
    return render_template("register.html", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password does not match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've been logged in!", "success")
                return redirect(url_for("index"))
            else:
                flash("Your email or password does not match!", "error")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out!", "success")
    return redirect(url_for("index"))


@app.route("/")
def index():
    context = {
        "tacos" : models.Taco.select(),
    } 
    return render_template("index.html", **context)


@app.route("/taco", methods=("GET", "POST"))
@login_required
def taco_create():
    form = forms.TacoForm()
    if form.validate_on_submit() or request.method=="POST":
        models.Taco.create(
            user=g.user._get_current_object(),
            protein=form.protein.data,
            shell=form.shell.data,
            cheese=form.cheese.data,
            extras=form.extras.data.strip(),
        )
        flash("Taco created!", "success")
        return redirect(url_for("index"))
    return render_template("taco.html", form=form)
       


if __name__ == "__main__":
    models.initialize_database()
    app.run(debug=DEBUG, host=HOST, port=PORT)



