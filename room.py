from classes import *


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