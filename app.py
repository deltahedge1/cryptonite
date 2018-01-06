from flask import Flask, request, redirect, url_for, render_template
from flask_restful import Resource, Api
from cryptocgt import Cryptotax
import jwt

cgtcalcultor = Cryptotax()

app = Flask(__name__)
app.secret_key = [r'\x903,J-H\xd4k`\x0e\x935\xb9\tX\xfe\x92p.\xeft\xd3\xc1\x07']
api = Api(app)

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

class Cryptonite2(Resource):
    def post(self):

        data =  request.get_json()
        data = data["data"]

        return(cgtcalcultor.calculateCGT(data))

api.add_resource(Cryptonite2, "/api/v1/cgt")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
