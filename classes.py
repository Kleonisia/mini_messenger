from config import *
from datetime import date, datetime

class Messages(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  date = db.Column(db.DateTime, default=datetime.now(), nullable=True)
  message = db.Column(db.String(500))

  def __repr__(self):
      user = User.query.filter(User.id == self.user_id).first()
      nickname = str(user).split(':')[3]
      return f'{nickname} ({self.date})>>>{self.message}'


class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)
  nickname = db.Column(db.String(50), unique=True)
  birthday = db.Column(db.Date, nullable=False)
  password = db.Column(db.String(500), nullable=False)

  def __repr__(self):
      return f'{self.password}:{self.id}:{self.name}:{self.nickname}:{self.birthday}'


class Room(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)
  creation_date = db.Column(db.Date, default=datetime.now(), nullable=True)

  def __repr__(self):
    return f'{self.name}:{self.id}'
