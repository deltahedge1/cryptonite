from flask import Flask, request, redirect, url_for, render_template, jsonify
from flask_restful import Resource, Api
from cryptocgt import Cryptotax
from flask_sqlalchemy import SQLAlchemy
import jwt
import uuid
import os
from functools import wraps
import wrapt
from flask_cors import CORS
from datetime import datetime
import json
import requests
from appconfig import APP_SECRET_KEY # this is an external file that has the secret key
from dbconfig import users_tbl #this is used to get and check security tokens
from sqlalchemy import select, update

basedir = os.path.abspath(os.path.dirname(__file__))

cgtcalculator = Cryptotax()

app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = APP_SECRET_KEY

try:
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
except:
    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'app.db')
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    except:
        pass

try:
    db = SQLAlchemy(app)
except:
    pass


class User(db.Model):
    #_id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(48), primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    password= db.Column(db.String(120))

    def __init__(self, name, email, public_id, password):
        self.name = name
        self.email = email
        self.public_id = public_id
        self.password = password

    def __repr__(self):
        return '<Name %r>' % self.name

api = Api(app)

#decorator for access main cryptonite api
def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if "x-access-token" not in request.headers:
            return ({"message":"x-access-token is missing from header"})

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        else:
            return ({"message":"token is missing"}, 401)

        if not token:
            return ({"message":"token is missing"}, 401)

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            public_id = data['public_id']
            try:
                selectQuery = users_tbl.select(users_tbl.c.public_id == public_id)
                result = list(selectQuery.execute())

                if result:
                    if result[0][4] == True:
                        return f(*args,**kwargs)
                    else:
                        return ({"message":"you are not an activated user"}, 401)
                else:
                    return ({"message":"public_id not found"}, 401)
            except:
                return ({"message": "an error occured and your token may or may not be valid"}, 500)
        except:
            return ({"message":"token is invalid"}, 401)

    return decorated

#decorator for admin api, checks if jwt decoded token for public_id for admin and then looks up admin from company column
def admin_token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None

        if "x-access-token" not in request.headers:
            return ({"message":"x-access-token is missing from header"})

        if "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        else:
            return ({"message":"token is missing"}, 401)

        if not token:
            return ({"message":"token is missing"}, 401)

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            public_id = data['public_id']
            try:
                selectQuery = users_tbl.select(users_tbl.c.public_id == public_id)
                result = list(selectQuery.execute())

                if result[0][2]=="admin":
                    return f(*args,**kwargs)
                else:
                    return ({"message":"forbidden not admin"}, 403)
            except Exception as e:
                return ({"message": str(e)}, 500)
        except:
            return ({"message":"token is invalid"}, 401)

    return decorated


@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        public_id = str(uuid.uuid4())
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        api_key = str(jwt.encode({"public_id": public_id}, app.config["SECRET_KEY"]).decode("utf-8"))

        user = User(public_id,name,email,password)
        db.session.rollback()
        db.session.add(user)
        db.session.commit()

        return render_template("success.html", name=name, api_key=api_key)

    return render_template("login.html")

class Test(Resource):
    @token_required
    def get(self):
        r = requests.get(r"https://api.fixer.io/latest")
        data = json.loads(r.text)
        return ({"message":r.text})

class Cryptonite(Resource):
    #class used to calcaulte CGT
    @token_required
    def post(self):

        capturedData =  request.get_json()
        data = capturedData["data"]

        if "entityType" not in capturedData:
            entityType = "Individual"
        else:
            entityType = capturedData["entityType"]

        return(cgtcalculator.calculateCGT(data,entityType))

class GetAttributes(Resource):
    #class used to get the entity types
    @token_required
    def get(self):
        return cgtcalculator.getEntityTypes()

class SecurityTokens(Resource):
    #get the security token of a user using the company name
    @admin_token_required
    def get(self, company):
        selectQuery = users_tbl.select(users_tbl.c.company == company)
        result = list(selectQuery.execute())

        if result:
            _id = result[0][0]
            public_id = result[0][1]
            company=result[0][2]
            token = result[0][3]
            active = result[0][4]

            return({"company": company, "public_id": public_id, "token":token, "active": active})
        else:
            return({"message":"no such company exists in the database"})


class PublicIdSecurityTokens(Resource):
    #get the security token of a user using the public id
    @admin_token_required
    def get(self, public_id):
        selectQuery = users_tbl.select(users_tbl.c.public_id == public_id)
        result = list(selectQuery.execute())

        if result:
            _id = result[0][0]
            public_id = result[0][1]
            company=result[0][2]
            token = result[0][3]
            active = result[0][4]

            return({"company": company, "public_id": public_id, "token":token, "active": active})
        else:
            return({"message":"no such public_id exists in the database"})

class AddSecurityTokens(Resource):
    @admin_token_required
    def post(self, company):
        #add users to the table unless they already exist
        try:
            selectQuery = users_tbl.select(users_tbl.c.company == company)
            result = list(selectQuery.execute())

            if result:
                return ({"message": "company already exists under that name pick a new one"})

            public_id = str(uuid.uuid4())
            #public_id = "818fb7e6-7074-4730-8bd8-cba675535280"
            token = str(jwt.encode({"public_id":public_id}, APP_SECRET_KEY, algorithm='HS256').decode("UTF-8"))
            users_tbl.insert().execute(public_id = public_id, token = token, company=company)
            return ({"message": "successfully created a new user", "company": company, "public_id":public_id, "token":token}, 201)

        except:
            return({"message": "unable to update database"}, 500)

class ChangeSecurityTokens(Resource):
    @admin_token_required
    def put(self, public_id):
        selectQuery = users_tbl.select(users_tbl.c.public_id == public_id)
        result = list(selectQuery.execute())

        if not result:
            return({"message":"no such public_id exists, token not changed"})

        if result:
            _id = result[0][0]
            #public_id = result[0][1]
            company=result[0][2]
            #token = result[0][3]
            active = result[0][4]

            new_public_id = str(uuid.uuid4())
            new_token=str(jwt.encode({"public_id":public_id}, APP_SECRET_KEY, algorithm='HS256').decode("UTF-8"))
            update_statement = users_tbl.update().where(users_tbl.c.public_id==public_id).values(public_id=new_public_id,token=new_token)
            update_statement.execute()

            return ({"message":"successfully updated user with new token","public_id":new_public_id,"company":company,"token":new_token,"active":active})

api.add_resource(Cryptonite, "/api/v1/cgt")
api.add_resource(GetAttributes, "/api/v1/entitytypes")
api.add_resource(Test, "/test")

api.add_resource(SecurityTokens, "/admin/gettoken/company/<string:company>") #GET request to get details using company name
api.add_resource(PublicIdSecurityTokens, "/admin/gettoken/publicid/<string:public_id>") #get request to get details using public_id
api.add_resource(AddSecurityTokens, "/admin/addtoken/company/<string:company>") #POST request to add a new user to the database and get the access token
api.add_resource(ChangeSecurityTokens, "/admin/changetoken/publicid/<string:public_id>") #PUT request to change a users token using their public_id

if __name__ == "__main__":
    app.run(debug=False)
