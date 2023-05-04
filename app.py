from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})
