from flask import Flask, redirect, render_template, request, url_for, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager

app = Flask(__name__)
app.secret_key = "!messenger!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)