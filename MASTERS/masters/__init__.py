from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# db variable initialization
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anirudh:Mumbai123@localhost:3306/masters_py'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 50
# export DATABASE_URL=mysql://anirudh:Mumbai123@localhost:3306/masters_py
# '
db = SQLAlchemy(app)


