from flask import Flask, request, redirect, url_for, render_template
from flask_restful import Resource, Api
from cryptocgt import Cryptotax
from flask_sqlalchemy import SQLAlchemy
import jwt
import uuid
import os

cgtcalcultor = Cryptotax()

app = Flask(__name__)
app.config["SECRET_KEY"] = 'aefaf674ac254f8ca6c1b6a73880aa55'
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(200), primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password= db.Column(db.String(120))

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.public_id = public_id
        self.password = password

    def __repr__(self):
        return '<Name %r>' % self.name


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        public_id = str(uuid.uuid4())

        api_key = jwt.encode({"public_id": public_id}, app.secret_key)
        api_key = str(jwt.encode({"public_id": public_id}, app.config["SECRET_KEY"]).decode("utf-8"))

        return render_template("success.html", name=name, api_key=api_key)

    return render_template("login.html")

class Cryptonite(Resource):
    def post(self):

        data =  request.get_json()
        data = data["data"]

        return(cgtcalcultor.calculateCGT(data))

api.add_resource(Cryptonite, "/api/v1/cgt")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
