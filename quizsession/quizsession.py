from flask import Blueprint, render_template, request, session
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from models import Quiz, QuestionCategory, Question, QuestionHasQuiz, db_session
from utils import parse_quiz_form_data

import ast

quizsession = Blueprint("quizsession", __name__, template_folder="templates", static_folder="static")


@quizsession.route("/choose-quiz")
def choose_quiz():

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

    return render_template("quizsession/choose_quiz.html", quizzes=quizzes)


@quizsession.route("/quiz-greeting/<int:quiz_id>")
def quiz_greeting(quiz_id):

    quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()

    return render_template("quizsession/quiz_greeting.html", quiz=quiz)


@quizsession.route("/quiz/<int:quiz_id>", methods=["GET", "POST"])
def quiz(quiz_id):

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

        # question_has_quiz_records = db_session.query(QuestionHasQuiz).filter_by(quiz_id=quiz_id).all()
        
        # for record in question_has_quiz_records:

        #     if not result[record.spørsmål_id]['answers']:
        #         db_session.add(QuizSession(spørsmål_har_quiz_id=record.id, svar_id=None, dato_tid=func.now()))
        #         continue

        #     for answer in result[record.spørsmål_id]['answers']:
        #         db_session.add(QuizSession(spørsmål_har_quiz_id=record.id, svar_id=answer, dato_tid=func.now()))

        db_session.commit()

        if 'passed_quizzes' not in session:
            session['passed_quizzes'] = [quiz_id]
        else:
            session['passed_quizzes'].append(quiz_id)
        
        session.modified = True

        return render_template(
            "quizsession/quiz_result.html",
            quiz=quiz,
            correct=len(list(filter(lambda question: question['correct'], result.values()))),
            particulary_correct=len(list(filter(lambda question: question['particulary_correct'], result.values()))),
            incorrect=len(list(filter(lambda question: question['incorrect'], result.values()))),
            not_answered=len(list(filter(lambda question: question['not_answered'], result.values()))),
            result=str(result)
        )

    return render_template("quizsession/quiz.html", quiz=quiz, questions=questions)


@quizsession.route("/quiz-result-details/<int:quiz_id>", methods=["POST"])
def quiz_result_details(quiz_id):

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
            "answer_options": {}
        }

        correct_answers = 0

        for answer_option in question.answer_options:

            answer_option_data = {
                "answer": answer_option.svar,
                "correct": answer_option.korrekt
            }

            correct_answers += answer_option.korrekt

            question_data["answer_options"][answer_option.id] = answer_option_data
        
        question_data["single_answer"] = correct_answers == 1
            
        questions.append(question_data)

    return render_template("quizsession/quiz_result_details.html", quiz=quiz, questions=questions, result=ast.literal_eval(request.form['quiz_result']))
