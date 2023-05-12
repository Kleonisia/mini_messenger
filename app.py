from flask import Flask, redirect, render_template, request, url_for, current_app, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, current_user, logout_user, login_required, UserMixin, LoginManager
from datetime import date, datetime

app = Flask(__name__)
app.secret_key = "!messenger!"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)

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


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@app.route('/')
def index():
  return redirect('/home')


@app.route('/home')
def home():
  return render_template('home.html')


@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    name = request.form.get('name')
    nickname = request.form.get('nickname')
    birthday = request.form.get('birthday')
    password = request.form.get('password')
    
    if not (name and nickname and birthday and password):
      flash("Введите данные корректно!", category="error")
    else:
      a, b, c = map(int, birthday.split('-'))
      user = User(name=name, nickname=nickname, birthday=date(a, b, c), password=password)
      db.session.add(user)
      db.session.commit()
      login_user(user, remember=True)
      flash("Вы успешно зарегистрировались", category="success")
      return redirect(url_for('profile', name=name, nickname=nickname, birthday=birthday, password=password)) # надо передавать POST-методом
  else:
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
  if request.method == "POST":
    nickname = request.form.get('nickname')
    password = request.form.get('password')
    a = User.query.filter(User.nickname == nickname).first()
    if not (nickname and password):
      flash("Введите данные корректно!", category="error")
    elif not a:
      flash("Неправильное имя пользователя", category="error")
    elif str(a).split(':')[0] != password:
      flash("Неправильный пароль", category="error")
    else:
      pswrd = str(a).split(':')[0]
      name = str(a).split(':')[2]
      nick = str(a).split(':')[3]
      birth = str(a).split(':')[4]
      login_user(a, remember=True)
      flash("Вы успешно вошли", category="success")
      return redirect(url_for('profile', name=name, nickname=nick, birthday=birth, password=pswrd)) # надо передавать POST-методом
  return render_template('login.html')


@app.route('/logout')
def logout():
  if current_user.is_anonymous:
    return redirect(url_for('login'))
  logout_user()
  return redirect(url_for('login'))


@app.route('/profile')
def profile():
  if current_user.is_anonymous:
    return redirect(url_for('login'))
  name = request.args.get('name')
  pswrd = request.args.get('password')
  nick = request.args.get('nickname')
  birth = request.args.get('birthday')
  return render_template('profile.html', name=name, pswrd=pswrd, nick=nick, birth=birth)


@app.route('/create_room', methods=["GET", "POST"])
def create_room():
  if current_user.is_anonymous:
    return redirect(url_for('login'))
  if request.method == "POST":
    room_name = request.form.get('name')
    a = User.query.filter(Room.name == room_name).first()
    if not room_name:
      flash("Введите данные корректно!", category="error")
    else:
      room = Room(name=room_name)
      db.session.add(room)
      db.session.commit()
      flash(f"Вы успешно создали комнату с именем {room_name}", category="success")
      return redirect(url_for('rooms'))
  return render_template('create_room.html')


@app.route('/rooms')
def rooms():
  if current_user.is_anonymous:
    return redirect(url_for('login'))
  return render_template("rooms.html", Room=Room)

@app.route('/room/<room_name>', methods=["GET", "POST"])
def room_message(room_name):
  if current_user.is_anonymous:
    return redirect(url_for('login'))
  room = Room.query.filter(Room.name == room_name).first() #
  room_id = str(room).split(':')[1] #
  if request.method == "POST":
    message = request.form.get('message') #
    user_name = current_user.nickname #
    user = User.query.filter(User.nickname == user_name).first() #
    user_id = str(user).split(':')[1]
    message = Messages(room_id=room_id, user_id=user_id, message=message)
    db.session.add(message)
    db.session.commit()
    return redirect(url_for('room_message', room_name=room_name))
  return render_template('room.html', name=current_user.nickname, Messages=Messages, room_name=room_name, room_id=room_id)

if __name__ == "__main__":
  app.run(debug=True)
  with app.app_context():
      db.create_all()
