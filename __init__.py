from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect

from admin.admin import admin
from quizsession.quizsession import quizsession
from quiz.quiz import quiz

from models import User, db_session

import config


app = Flask(__name__)

csrf = CSRFProtect(app)

app.config.from_object(config.DevelopmentConfig)

app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(quizsession, url_prefix="/quizsession")
app.register_blueprint(quiz, url_prefix="/quiz")

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(_id):

    _admin = User(id=_id)

    _admin.set_info(**db_session.query(User).filter_by(id=_id).first().__dict__)

    return _admin


@app.errorhandler(401)
def unauthorized_error(error):
    return redirect(url_for('index'))


@app.route("/")
def index():

    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_profile'))

    return render_template("index.html")


if __name__ == "__main__":
    app.run()
