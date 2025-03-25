from classes import *

@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "POST":
    name = request.form.get('name')
    nickname = request.form.get('nickname')
    birthday = request.form.get('birthday')
    password = request.form.get('password')
    if not (name and nickname and birthday and password):
      flash("Введите данные корректно!", category="error")
    elif User.query.filter(User.nickname == nickname).count() != 0:
      flash("Такое имя пользователя уже существует", category="error")
      return render_template('register.html')
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
