from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
from sqlalchemy.exc import IntegrityError

from models import Admin, Quiz, Question, QuestionCategory, db_session
from forms import LoginForm, RegistrationForm, AddCategoryForm


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin.route("/user-login", methods=["GET", "POST"])
def user_login():

    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_profile"))

    login_form = LoginForm()

    if login_form.validate_on_submit():

        try:

            user = db_session.query(Admin).filter_by(login=login_form.login.data).first()

            if not user:

                flash(f"Det finnes ingen bruker med påloggingen '{login_form.login.data}'.", category="error")

                return redirect(url_for("admin.user_login"))

            if not cph(user.passord, login_form.password.data):

                flash(f"Feil passord for påloggingen '{login_form.login.data}'.", category="error")

                return redirect(url_for("admin.user_login"))

            login_user(user)

            flash(f"Velkommen {user.login}!", category="success")

            return redirect(url_for("admin.admin_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("admin.user_login"))

    return render_template("admin/user_login.html", login_form=login_form)


@admin.route("/user-registration", methods=["GET", "POST"])
def user_registration():

    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_profile"))

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():

        try:
        
            user = Admin(
                login=registration_form.login.data,
                fornavn=registration_form.first_name.data,
                etternavn=registration_form.last_name.data,
                passord=gph(registration_form.password.data, salt_length=16)
            )

            db_session.add(user)

            db_session.commit()

            login_user(user)

            flash(f"Velkommen {user.login}!", category="success")

            return redirect(url_for("admin.admin_profile"))

        except IntegrityError:

            db_session.rollback()

            flash(f"Det finnes allerede en bruker med påloggingen '{registration_form.login.data}'.", category="error")

            return redirect(url_for("admin.user_registration"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("admin.user_registration"))

    elif request.method == "POST":
        
        if 'password_confirm' in registration_form.errors:    
            flash("Passordene må være like.", category="error")
        else:
            flash(str(registration_form.errors), category="error")
        
        return redirect(url_for("admin.user_registration"))

    return render_template("admin/user_registration.html", registration_form=registration_form)


@admin.route("/admin-profile")
@login_required
def admin_profile():

    quizzes = db_session.query(Quiz).filter_by(admin_id=current_user['id']).all()

    questions = db_session.query(Question).filter_by(admin_id=current_user['id']).all()

    categories = db_session.query(QuestionCategory).all()

    add_category_form = AddCategoryForm()

    return render_template("admin/admin_profile.html", quizzes=quizzes, questions=questions, categories=categories, add_category_form=add_category_form)


@admin.route("/user-logout")
@login_required
def user_logout():

    logout_user()

    return redirect(url_for("index"))
