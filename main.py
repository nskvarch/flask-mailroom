import os
from passlib.hash import pbkdf2_sha256
from flask import Flask, render_template, request, redirect, url_for, session
from model import Donation, Donor, User

app = Flask(__name__)
# app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

app.secret_key = os.environ.get("SECRET_KEY").encode()


@app.route("/")
def home():
    return redirect(url_for("list_all"))


@app.route("/donations/")
def list_all():
    donations = Donation.select()
    return render_template("donations.jinja2", donations=donations)


@app.route("/add", methods=["GET", "POST"])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        # try:
        new_donation = Donor.select().where(Donor.name == request.form["donor"])
        Donation(id=new_donation, value=request.form["donation_amount"]).save()
        # for some reason Alice is also Bob but Charlie works when adding donations?

        # tried to catch unknown donors
        # except Donation.DoesNotExist:
        # return render_template("add.jinja2", error="That Donor is not yet in the database.")
        # new_donor = Donor(name=request.form["donor_name"])
        # new_donor.save()
        # new_value = Donation(donor=new_donor, value=request.form["donation_amount"])
        # new_value.save()
        return redirect(url_for('list_all'))

    else:
        return render_template("add.jinja2")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            user = User.select().where(User.username == request.form["username"]).get()
        except User.DoesNotExist:
            return render_template("login.jinja2", error="Incorrect Username and or Password")

        if user and pbkdf2_sha256.hash(request.form["username"]):
            session["username"] = request.form["username"]
            return redirect(url_for("add"))

        else:
            return render_template("login.jinja2", error="Incorrect Username and or Password")

    else:
        return render_template("login.jinja2")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host="0.0.0.0", port=port)
