import os
from flask import Flask, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:postgres@localhost/testapi"

db=SQLAlchemy(app)

with app.app_context():
    db.create_all()

"""
to create db from model :
    python
    >>> from app import app, db
    >>> app.app_context().push()
    >>> db.create_all()
"""

class Testuser(db.Model):
    __tablename__ = 'testuser'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(40))
    password=db.Column(db.String(40))


    def __int__(self,username,password):
        self.username = username
        self.password = password


@app.route("/", methods=['GET'])
def index():
    return jsonify(health_check = "OK"),200

@app.route("/<string:path_var>")
def get_path_variable(path_var: str):
    return jsonify(data = path_var),200

@app.route("/postit", methods=['POST'])
def postreq():
    req = request.json
    name = req['name']
    responseMessage = name + " logged in succesfully"
    return jsonify(message=responseMessage)

@app.route("/adduser",methods=['POST'])
def addUser():
    req = request.json
    username = req['username']
    password = req['password']

    #user = User(name,password)
    user = Testuser(username=username,password =password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="True")



if __name__ == "__main__":
    app.run()