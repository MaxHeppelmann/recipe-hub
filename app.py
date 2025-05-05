from flask import Flask, render_template,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import text
import dotenv
import os
import random
dotenv.load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://ubuntu:{os.environ.get('POSTGRESPASSWORD')}@localhost:5432/recipe-db'
db = SQLAlchemy(app)
class users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)
class recipes(db.Model):
    __tablename__='recipes'
    id = db.Column(db.Integer,primary_key = True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False)
    ingredients = db.Column(ARRAY(db.String(100)),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
@app.route('/',methods=['GET'])
def landing_page():
    result=users.query.all()
    return render_template('index.html',jinjvar="Jinja2",userList=result)
@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        handleLogin(request.json)
        return {"status":200}
    return "<h1><b>error</b></h1>"

def initialize_db():
    db.create_all()
    print("DB created")



def handleLogin(data):
    potentialUser=users.query.filter_by(username=data['username']).first()
    if potentialUser:
        if potentialUser.passwordHash==data['password']:
            return {"status":200}
        else:
            return {"status":401}
    else:
        return "<h1><b>no user found</b></h1>"
if __name__ == '__main__':
    initialize_db()
    app.run()