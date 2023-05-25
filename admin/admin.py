from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import User, Quiz, Question, QuestionCategory, QuestionHasQuiz, QuizSession, QuizSessionAnswer, db_session
from forms import LoginForm, RegistrationForm, AddCategoryForm


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_profile"))

    login_form = LoginForm()

    if login_form.validate_on_submit():

        try:

            user = db_session.query(User).filter_by(login=login_form.login.data).first()

            if not user:

                flash(f"Det finnes ingen bruker med påloggingen '{login_form.login.data}'.", category="error")

                return redirect(url_for("admin.admin_login"))

            if not cph(user.passord, login_form.password.data):

                flash(f"Feil passord for påloggingen '{login_form.login.data}'.", category="error")

                return redirect(url_for("admin.admin_login"))

            login_user(user)

            flash(f"Velkommen {user.login}!", category="success")

            return redirect(url_for("admin.admin_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("admin.admin_login"))

    return render_template("admin/admin_login.html", login_form=login_form)


@admin.route("/admin-registration", methods=["GET", "POST"])
def admin_registration():

    if current_user.is_authenticated:
        return redirect(url_for("admin.admin_profile"))

    registration_form = RegistrationForm()

    if registration_form.validate_on_submit():

        try:
        
            user = User(
                login=registration_form.login.data,
                fornavn=registration_form.first_name.data,
                etternavn=registration_form.last_name.data,
                passord=gph(registration_form.password.data, salt_length=16),
                admin=True
            )

            db_session.add(user)

            db_session.commit()

            login_user(user)

            flash(f"Velkommen {user.login}!", category="success")

            return redirect(url_for("admin.admin_profile"))

        except IntegrityError:

            db_session.rollback()

            flash(f"Det finnes allerede en bruker med påloggingen '{registration_form.login.data}'.", category="error")

            return redirect(url_for("admin.admin_registration"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("admin.admin_registration"))

    elif request.method == "POST":
        
        if 'password_confirm' in registration_form.errors:    
            flash("Passordene må være like.", category="error")
        else:
            flash(str(registration_form.errors), category="error")
        
        return redirect(url_for("admin.admin_registration"))

    return render_template("admin/admin_registration.html", registration_form=registration_form)


@admin.route("/admin-profile")
@login_required
def admin_profile():

    quizzes = db_session.query(Quiz).filter_by(admin_id=current_user['id']).all()

    questions = db_session.query(Question).filter_by(admin_id=current_user['id']).all()

    categories = db_session.query(QuestionCategory).all()

    add_category_form = AddCategoryForm()

    return render_template("admin/admin_profile.html", quizzes=quizzes, questions=questions, categories=categories, add_category_form=add_category_form)


@admin.route("/assessment")
@login_required
def assessment():

    quiz_sessions = (
        db_session.query(
            QuizSession.id,
            QuizSession.godkjent,
            Quiz.navn,
            Quiz.beskrivelse,
            func.count(func.distinct(QuestionHasQuiz.spørsmål_id)).label('number_of_questions'),
            func.group_concat(QuestionCategory.navn, ',').label('categories'),
            Quiz.admin_id
        ).join(Quiz, QuizSession.quiz_id == Quiz.id)
        .join(QuestionHasQuiz, Quiz.id == QuestionHasQuiz.quiz_id)
        .join(Question, QuestionHasQuiz.spørsmål_id == Question.id)
        .join(QuestionCategory, Question.kategori_id == QuestionCategory.id)
        .group_by(QuizSession.id)
        .all()
    )

    quiz_sessions = list(filter(lambda qs: qs['admin_id'] == current_user['id'], map(
        lambda row: {
            'id': row[0], 'approved': row[1], 'name': row[2], 'description': row[3], 'number_of_questions': row[4],
            'categories': list(set(filter(bool, row[5].split(',')))), 'admin_id': row[6]
        },
        quiz_sessions
    )))

    return render_template("admin/assessment.html", quiz_sessions=quiz_sessions)


@admin.route("/admin-logout")
@login_required
def admin_logout():

    logout_user()

    return redirect(url_for("index"))
