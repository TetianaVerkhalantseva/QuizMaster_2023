from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from models import Quiz, QuestionCategory, Question, QuestionHasQuiz, QuizSession, QuizSessionQuestion, QuizSessionAnswer, db_session, QuizComment, QuestionComment
from utils import parse_quiz_form_data

import ast

from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegistrationForm, AddCategoryForm

from models import User, Quiz, Question, QuestionCategory, db_session

from werkzeug.security import generate_password_hash as gph, check_password_hash as cph

from sqlalchemy.exc import IntegrityError


student = Blueprint("student", __name__, template_folder="templates", static_folder="static")


@student.route("/student-login", methods=["GET", "POST"])
def student_login():

    if current_user.is_authenticated:

        if current_user['admin']:
            return redirect(url_for("admin.admin_profile"))
        else:
            return redirect(url_for("student.student_profile"))

    login_form = LoginForm()

    if login_form.validate_on_submit():

        try:

            user = db_session.query(User).filter_by(login=login_form.login.data).filter_by(admin=False).first()

            if not user:

                flash(f"Det finnes ingen student bruker med brukernavn '{login_form.login.data}'.", category="error")

                return redirect(url_for("student.student_login"))

            if not cph(user.passord, login_form.password.data):

                flash(f"Feil passord for brukernavn '{login_form.login.data}'.", category="error")

                return redirect(url_for("student.student_login"))

            login_user(user)

            flash(f"Velkommen {user.login}!", category="success")

            return redirect(url_for("student.student_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("student.student_login"))

    return render_template("student/student_login.html", login_form=login_form)


@student.route("/student-registration", methods=['POST', 'GET'])
def student_registration():

    if current_user.is_authenticated:

        if current_user['admin']:
            return redirect(url_for("admin.admin_profile"))
        else:
            return redirect(url_for("student.student_profile"))
        
        
    form = RegistrationForm()

    if form.validate_on_submit():

        try:
            student = User(
                login = form.login.data,
                fornavn = form.first_name.data,
                etternavn = form.last_name.data,
                passord = gph(form.password.data, salt_length=16),
                admin = False
            )

            db_session.add(student)
            db_session.commit()

            login_user(student)

            flash(f"Velkommen {student.fornavn} {student.etternavn}!", category="success")

            return redirect(url_for("student.student_profile"))
        
        except IntegrityError:
            
            db_session.rollback()

            flash(f"Det finnes allerede en bruker med brukernavn '{form.login.data}'.", category="error")

            return redirect(url_for("admin.admin_registration"))
        
        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("student.student_registration"))

    elif request.method == 'POST':

        if 'password_confirm' in form.errors:
            flash("Passordene må være like!", category="error")
        else:
            flash(str(form.errors), category="error")
    
    return render_template("student/student_registration.html", form=form)
    

@student.route("/student-profile")
@login_required
def student_profile():

    if current_user['admin']:
        return redirect(url_for("admin.admin_profile"))

    else:
        quizzes = (
            db_session.query(
                Quiz.id,
                Quiz.navn,
                Quiz.beskrivelse,
                func.count(func.distinct(QuestionHasQuiz.spørsmål_id)).label('number_of_questions'),
                func.group_concat(QuestionCategory.navn, ',').label('categories')
            )
            .join(QuestionHasQuiz, Quiz.id == QuestionHasQuiz.quiz_id)
            .join(Question, QuestionHasQuiz.spørsmål_id == Question.id)
            .join(QuestionCategory, Question.kategori_id == QuestionCategory.id)
            .group_by(Quiz.id, Quiz.navn)
            .all()
        )

        quizzes = list(map(
            lambda row: {
                'id': row[0], 'name': row[1], 'description': row[2], 'number_of_questions': row[3], 'categories': list(set(filter(bool, row[4].split(','))))
            },
            quizzes
        ))

        return render_template("student/student_profile.html", quizzes=quizzes)


@student.route("/student-assessment")
@login_required
def student_assessment():
    
    if current_user['admin']:
        return redirect(url_for("admin.assessment"))
    
    quizzes = (
        db_session.query(
            Quiz.id,
            Quiz.navn,
            Quiz.beskrivelse,
            QuizSession.id,
            QuizSession.godkjent,
            func.count(func.distinct(QuestionHasQuiz.spørsmål_id)).label('number_of_questions'),
            func.group_concat(QuestionCategory.navn, ',').label('categories')
        )
        .join(QuizSession, Quiz.id == QuizSession.quiz_id)
        .join(QuestionHasQuiz, Quiz.id == QuestionHasQuiz.quiz_id)
        .join(Question, QuestionHasQuiz.spørsmål_id == Question.id)
        .join(QuestionCategory, Question.kategori_id == QuestionCategory.id)
        .group_by(Quiz.id)
        .all()
    )

    quizzes = list(map(
        lambda row: {
            'id': row[0], 'name': row[1], 'description': row[2], 'quiz_session_id': row[3], 'approved': row[4], 'number_of_questions': row[5], 'categories': list(set(filter(bool, row[6].split(','))))
        },
        quizzes
    ))
    
    return render_template("student/student_assessment.html", quizzes=quizzes)


@student.route("/quiz-greeting/<int:quiz_id>")
@login_required
def quiz_greeting(quiz_id):

    if current_user['admin']:
        return redirect(url_for("admin.admin_profile"))

    quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()

    return render_template("student/quiz_greeting.html", quiz=quiz)


@student.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def quiz(quiz_id):

    if current_user['admin']:
        return redirect(url_for("admin.admin_profile"))

    quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()

    questions_from_db = (
        db_session.query(Question)
        .join(QuestionHasQuiz)
        .filter(QuestionHasQuiz.quiz_id == quiz_id)
        .options(joinedload(Question.answer_options))
        .all()
    )

    questions = []

    for question in questions_from_db:

        question_data = {
            "id": question.id,
            "question": question.spørsmål,
            "answer_options": []
        }

        correct_answers = 0

        for answer_option in question.answer_options:

            answer_option_data = {
                "id": answer_option.id,
                "answer": answer_option.svar,
                "correct": answer_option.korrekt
            }

            correct_answers += answer_option.korrekt

            question_data["answer_options"].append(answer_option_data)
        
        question_data["single_answer"] = correct_answers == 1
            
        questions.append(question_data)

    if request.method == "POST":

        result = parse_quiz_form_data(questions, request.form)

        quiz_session = QuizSession(quiz_id=quiz_id, student_id=1, godkjent=0)

        db_session.add(quiz_session)

        db_session.commit()

        for question_id in result:

            quiz_session_question = QuizSessionQuestion(quiz_sesjon_id=quiz_session.id, spørsmål_id=question_id, godkjent=0)

            db_session.add(quiz_session_question)

            db_session.commit()

            if not result[question_id]['answers']:
                continue

            for answer in result[question_id]['answers']:
                db_session.add(QuizSessionAnswer(quiz_sesjon_spørsmål_id=quiz_session_question.id, svarmulighet_id=answer))

        db_session.commit()

        if 'passed_quizzes' not in session:
            session['passed_quizzes'] = [quiz_id]
        else:
            session['passed_quizzes'].append(quiz_id)
        
        session.modified = True

        if current_user['admin']:

            return redirect(url_for("admin.assessment"))
        
        else:

            flash(f"Du har sendt inn quiz!", category="success")

            return redirect(url_for("student.student_profile"))

    return render_template("student/quiz.html", quiz=quiz, questions=questions)


@student.route("/quiz-result-details/<int:quiz_session_id>")
@login_required
def quiz_result_details(quiz_session_id):

    if current_user['admin']:
        return redirect(url_for("admin.admin_profile"))

    quiz_session = db_session.query(QuizSession).filter_by(id=quiz_session_id).first()

    quiz = db_session.query(Quiz).filter_by(id=quiz_session.quiz_id).first()

    questions_from_db = (
        db_session.query(Question)
        .join(QuestionHasQuiz)
        .filter(QuestionHasQuiz.quiz_id == quiz.id)
        .options(joinedload(Question.answer_options))
        .all()
    )

    questions = []

    for question in questions_from_db:

        question_data = {
            "id": question.id,
            "question": question.spørsmål,
            "answer_options": {}
        }

        for answer_option in question.answer_options:

            answer_option_data = {
                "id": answer_option.id,
                "answer": answer_option.svar,
            }

            question_data["answer_options"][answer_option.id] = answer_option_data
            
        questions.append(question_data)

    result = {}

    for question in questions:

        quiz_session_answers = list(filter(
            lambda ao: ao.svarmulighet_id is not None,
            db_session.query(QuizSessionAnswer).filter_by(spørsmål_id=question['id'], quiz_sesjon_id=quiz_session_id).all()
        ))

        answers = {}

        for ao in quiz_session_answers:
            answers[ao.svarmulighet_id] = {'answer': question['answer_options'][ao.svarmulighet_id]['answer']}

        question_not_answered = len(answers) == 0

        result[question['id']] = {'answers': answers, 'not_answered': question_not_answered}

    return render_template("student/quiz_result_details.html", quiz_session=quiz_session, quiz=quiz, questions=questions, result=result)



@student.route("/student-logout")
@login_required
def student_logout():

    if current_user['admin']:
        return redirect(url_for("admin.admin_profile"))

    logout_user()

    return redirect(url_for("index"))
