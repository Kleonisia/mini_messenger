from user import *
from room import *


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


@app.route('/')
def index():
  return redirect('/home')


@app.route('/home')
def home():
  return render_template('home.html')


if __name__ == "__main__":
  app.run(debug=True)
  with app.app_context():
      db.create_all()
