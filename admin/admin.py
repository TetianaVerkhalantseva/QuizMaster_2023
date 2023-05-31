from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash as gph, check_password_hash as cph
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from models import User, Quiz, Question, QuestionCategory, QuestionHasQuiz, QuizSession, QuizSessionQuestion, QuizSessionAnswer, QuizComment, QuestionComment, db_session
from forms import LoginForm, RegistrationForm, AddCategoryForm


admin = Blueprint("admin", __name__, template_folder="templates", static_folder="static")


@admin.route("/admin-login", methods=["GET", "POST"])
def admin_login():

    if current_user.is_authenticated:

        if current_user['admin']:
            return redirect(url_for("admin.admin_profile"))
        else:
            return redirect(url_for("student.student_profile"))

    login_form = LoginForm()

    if login_form.validate_on_submit():

        try:

            user = db_session.query(User).filter_by(login=login_form.login.data).filter_by(admin=True).first()

            if not user:

                flash(f"Det finnes ingen admin bruker med brukernavn '{login_form.login.data}'.", category="error")

                return redirect(url_for("admin.admin_login"))

            if not cph(user.passord, login_form.password.data):

                flash(f"Feil passord for brukernavn '{login_form.login.data}'.", category="error")

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

        if current_user['admin']:
            return redirect(url_for("admin.admin_profile"))
        else:
            return redirect(url_for("student.student_profile"))

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

            flash(f"Det finnes allerede en bruker med brukernavn '{registration_form.login.data}'.", category="error")

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

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))

    quizzes = db_session.query(Quiz).filter_by(admin_id=current_user['id']).all()

    questions = db_session.query(Question).filter_by(admin_id=current_user['id']).all()

    categories = db_session.query(QuestionCategory).all()

    add_category_form = AddCategoryForm()

    return render_template("admin/admin_profile.html", quizzes=quizzes, questions=questions, categories=categories, add_category_form=add_category_form)


@admin.route("/assessment")
@login_required
def assessment():

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))

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


@admin.route("/quiz-session-details/<int:quiz_session_id>")
@login_required
def quiz_session_details(quiz_session_id):

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))
    
    init_selected = request.args.get('initSelected', 1, type=int)

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

        correct_answers = 0

        for answer_option in question.answer_options:

            answer_option_data = {
                "id": answer_option.id,
                "answer": answer_option.svar,
                "correct": answer_option.korrekt
            }

            correct_answers += answer_option.korrekt

            question_data["answer_options"][answer_option.id] = answer_option_data
        
        question_data["single_answer"] = correct_answers == 1
            
        questions.append(question_data)

    result = {}

    for question in questions:

        quiz_session_question = db_session.query(QuizSessionQuestion).filter_by(spørsmål_id=question['id'], quiz_sesjon_id=quiz_session_id).first()

        quiz_session_answers = db_session.query(QuizSessionAnswer).filter_by(quiz_sesjon_spørsmål_id=quiz_session_question.id).all()

        answers = {}

        for ao in quiz_session_answers:
            answers[ao.svarmulighet_id] = {'correct': question['answer_options'][ao.svarmulighet_id]['correct']}

        text_answer = not question['answer_options']

        question_not_answered = len(answers) == 0 if not text_answer else not quiz_session_question.tekstsvar
        question_correct = all([answer['correct'] for answer in answers.values()]) and set(answers.keys()) == set([ao['id'] for ao in question['answer_options'].values() if ao['correct']]) and not question_not_answered
        question_incorrect = not any([answer['correct'] for answer in answers.values()]) and not question_not_answered
        question_particulary_correct = not question_correct and not question_incorrect and not question_not_answered

        question_comment = db_session.query(QuestionComment).filter_by(quiz_sesjon_spørsmål_id=quiz_session_question.id).first()

        result[question['id']] = {
            'text_answer': text_answer, 'answer_text': quiz_session_question.tekstsvar,
            'comment': question_comment.tekst if question_comment else None,
            'quiz_session_question_id': quiz_session_question.id,
            'answers': answers, 'correct': question_correct, 'particulary_correct': question_particulary_correct,
            'incorrect': question_incorrect, 'not_answered': question_not_answered, 'approved': quiz_session_question.godkjent
        }

        quiz_session_comment = db_session.query(QuizComment).filter_by(quiz_sesjon_id=quiz_session_id).first()

    return render_template("admin/quiz_session_details.html", quiz_session=quiz_session, quiz=quiz, questions=questions, result=result, init_selected=init_selected, quiz_session_comment=quiz_session_comment)


@admin.route("/approve-quiz-session/<int:quiz_session_id>")
@login_required
def approve_quiz_session(quiz_session_id):
    
        if not current_user['admin']:
            return redirect(url_for("student.student_profile"))
    
        quiz_session = db_session.query(QuizSession).filter_by(id=quiz_session_id).first()
    
        quiz_session.godkjent = True

        quiz_session_questions = db_session.query(QuizSessionQuestion).filter_by(quiz_sesjon_id=quiz_session_id).all()

        for quiz_session_question in quiz_session_questions:
            quiz_session_question.godkjent = True
    
        db_session.commit()
    
        return redirect(url_for("admin.quiz_session_details", quiz_session_id=quiz_session_id))


@admin.route("/approve-quiz-session-question/<int:quiz_session_id>/<int:question_id>")
@login_required
def approve_quiz_session_question(quiz_session_id, question_id):

    init_selected = request.args.get('initSelected', 1, type=int)

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))

    quiz_session_questions = db_session.query(QuizSessionQuestion).filter_by(quiz_sesjon_id=quiz_session_id).all()

    for quiz_session_question in filter(lambda qsq: qsq.spørsmål_id == question_id, quiz_session_questions):
        quiz_session_question.godkjent = True

    db_session.commit()

    if all([qsq.godkjent for qsq in quiz_session_questions]):
        
        quiz_session = db_session.query(QuizSession).filter_by(id=quiz_session_id).first()
        quiz_session.godkjent = True

        db_session.commit()

    return redirect(url_for("admin.quiz_session_details", quiz_session_id=quiz_session_id, initSelected=init_selected))


@admin.route("/comment-quiz-session/<int:quiz_session_id>", methods=["POST"])
@login_required
def comment_quiz_session(quiz_session_id):

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))

    quiz_comment = QuizComment(quiz_sesjon_id=quiz_session_id, bruker_id=current_user['id'], tekst=request.form['comment'])

    db_session.add(quiz_comment)

    db_session.commit()

    return redirect(url_for("admin.quiz_session_details", quiz_session_id=quiz_session_id))


@admin.route("/comment-quiz-session-question/<int:quiz_session_question_id>", methods=["POST"])
@login_required
def comment_quiz_session_question(quiz_session_question_id):

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))

    init_selected = request.args.get('initSelected', 1, type=int)

    quiz_session_question = db_session.query(QuizSessionQuestion).filter_by(id=quiz_session_question_id).first()

    question_comment = QuestionComment(quiz_sesjon_spørsmål_id=quiz_session_question_id, bruker_id=current_user['id'], tekst=request.form['comment'])

    db_session.add(question_comment)

    db_session.commit()

    return redirect(url_for("admin.quiz_session_details", quiz_session_id=quiz_session_question.quiz_sesjon_id, initSelected=init_selected))


@admin.route("/admin-logout")
@login_required
def admin_logout():

    if not current_user['admin']:
        return redirect(url_for("student.student_profile"))

    logout_user()

    return redirect(url_for("index"))
