from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func

from models import Quiz, Question, QuestionCategory, AnswerOption, QuestionHasQuiz, db_session


quiz = Blueprint("quiz", __name__, template_folder="templates", static_folder="static")


@quiz.route("/quiz-details<int:quiz_id>")
@login_required
def quiz_details(quiz_id):

    _quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()
    
    question_ids = [record.spørsmål_id for record in db_session.query(QuestionHasQuiz).filter_by(quiz_id=quiz_id).all()]

    questions = db_session.query(Question).filter(Question.id.in_(question_ids)).all()

    return render_template("quiz/quiz_details.html", quiz=_quiz, questions=questions)


@quiz.route("/remove-quiz/<int:quiz_id>")
@login_required
def remove_quiz(quiz_id):

    try:

        quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()

        question_has_quiz_records = db_session.query(QuestionHasQuiz).filter_by(quiz_id=quiz_id).all()

        for record in question_has_quiz_records:

            # quiz_session_records = db_session.query(QuizSession).filter_by(spørsmål_har_quiz_id=record.id).all()

            # for quiz_session_record in quiz_session_records:
            #    db_session.delete(quiz_session_record)

            db_session.delete(record)

        db_session.delete(quiz)

        db_session.commit()

        flash(f"Quizzen '{quiz.navn}' er nå slettet.", category="success")

        return redirect(url_for("admin.admin_profile"))

    except Exception as exception:

        flash(f"{type(exception).__name__}: {exception}", category="error")

        return redirect(url_for("admin.admin_profile"))


@quiz.route("/add-quiz", methods=["GET", "POST"])
@login_required
def add_quiz():

    questions = db_session.query(Question).filter_by(admin_id=current_user.id).all()

    if request.method == "POST":

        try:

            _quiz = Quiz(navn=request.form["quiz_name"], beskrivelse=request.form['description'], admin_id=current_user.id)

            db_session.add(_quiz)

            db_session.commit()

            question_ids = [int(key) for key in request.form.keys() if key.isnumeric()]

            for question_id in question_ids:

                question_has_quiz = QuestionHasQuiz(spørsmål_id=question_id, quiz_id=_quiz.id)

                db_session.add(question_has_quiz)

            db_session.commit()

            flash(f"Quizzen '{request.form['quiz_name']}' er nå lagt til.", category="success")

            return redirect(url_for("admin.admin_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("admin.admin_profile"))

    return render_template("quiz/add_quiz.html", questions=questions)


@quiz.route("/edit-quiz/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def edit_quiz(quiz_id):

    _quiz = db_session.query(Quiz).filter_by(id=quiz_id).first()
    questions = db_session.query(Question).filter_by(admin_id=current_user.id).all()
    quiz_question_ids = [record.spørsmål_id for record in db_session.query(QuestionHasQuiz).filter_by(quiz_id=quiz_id).all()]

    if request.method == "POST":
        
        try:
            
            _quiz.navn = request.form["quiz_name"]
            _quiz.beskrivelse = request.form["description"]

            db_session.commit()

            question_has_quiz_records = db_session.query(QuestionHasQuiz).filter_by(quiz_id=quiz_id).all()

            for record in question_has_quiz_records:

                # quiz_session_records = db_session.query(QuizSession).filter_by(spørsmål_har_quiz_id=record.id).all()

                # for quiz_session_record in quiz_session_records:
                #    db_session.delete(quiz_session_record)

                db_session.delete(record)

            db_session.commit()

            question_ids = [int(key) for key in request.form.keys() if key.isnumeric()]

            for question_id in question_ids:

                question_has_quiz = QuestionHasQuiz(spørsmål_id=question_id, quiz_id=_quiz.id)

                db_session.add(question_has_quiz)

            db_session.commit()

            flash(f"Quizzen '{request.form['quiz_name']}' er nå oppdatert.", category="success")

            return redirect(url_for("admin.admin_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return redirect(url_for("admin.admin_profile"))

    return render_template("quiz/edit_quiz.html", quiz=_quiz, questions=questions, quiz_question_ids=quiz_question_ids)


@quiz.route("/question-details<int:question_id>")
@login_required
def question_details(question_id):

    question = db_session.query(Question).filter_by(id=question_id).first()

    answers = db_session.query(AnswerOption).filter_by(spørsmål_id=question_id).all()

    answers_details = []

    # for answer in answers:
    #    answers_details.append({"answer": answer.svar, "correct": answer.korrekt, "number_of_answers": db_session.query(QuizSession).filter_by(svar_id=answer.id).count()})

    return render_template("quiz/question_details.html", question=question, answers=answers, answers_details=answers_details)


@quiz.route("/remove-question/<int:question_id>")
@login_required
def remove_question(question_id):
    
    try:
        
        question = db_session.query(Question).filter_by(id=question_id).first()

        answers = db_session.query(AnswerOption).filter_by(spørsmål_id=question_id).all()

        question_has_quiz_records = db_session.query(QuestionHasQuiz).filter_by(spørsmål_id=question_id).all()

        for record in question_has_quiz_records:
            
            # qiuz_session_records = db_session.query(QuizSession).filter_by(spørsmål_har_quiz_id=record.id).all()

            # for quiz_session_record in qiuz_session_records:
            #        db_session.delete(quiz_session_record)

            db_session.delete(record)

        for answer in answers:
            db_session.delete(answer)

        db_session.delete(question)
        
        db_session.commit()
        
        flash(f"Spørsmålet '{question.spørsmål}' er nå slettet.", category="success")
        
        return redirect(url_for("admin.admin_profile"))
    
    except Exception as exception:
        
        flash(f"{type(exception).__name__}: {exception}", category="error")
        
        return redirect(url_for("admin.admin_profile"))


@quiz.route("/add-question", methods=["GET", "POST"])
@login_required
def add_question():

    categories = db_session.query(QuestionCategory).all()

    if request.method == "POST":

        answers = []

        i = 1

        while f"answer-{i}" in request.form:

            answers.append({"svar": request.form.get(f"answer-{i}"), "korrekt": f"correct-{i}" in request.form})

            i += 1
        
        try:

            if len(answers) == 1:

                flash("Spørsmål må ha minst to svaralternativer. Eneste unntak er et type spørsmål (essay).", category="error")

                return render_template("quiz/add_question.html", answers=answers, categories=categories, question=request.form.get("question"), category_id=request.form.get("category-select"))

            if answers and not any([answer["korrekt"] for answer in answers]):
                
                flash("Spørsmål må ha minst ett korrekt svaralternativ.", category="error")

                return render_template("quiz/add_question.html", answers=answers, categories=categories, question=request.form.get("question"), category_id=request.form.get("category-select"))

            question = Question(spørsmål=request.form.get("question"), kategori_id=request.form.get("category-select"), admin_id=current_user.id)

            db_session.add(question)

            db_session.commit()

            for answer in answers:

                answer_option = AnswerOption(spørsmål_id=question.id, svar=answer["svar"], korrekt=answer["korrekt"])

                db_session.add(answer_option)
            
            db_session.commit()

            flash(f"Spørsmålet '{question.spørsmål}' er nå lagt til.", category="success")

            return redirect(url_for("admin.admin_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return render_template("quiz/add_question.html", answers=answers, categories=categories, question=request.form.get("question"), category_id=request.form.get("category-select"))

    return render_template("quiz/add_question.html", answers=[], categories=categories, question=None, category_id=None)


@quiz.route("/edit-question/<int:question_id>", methods=["GET", "POST"])
@login_required
def edit_question(question_id):

    categories = db_session.query(QuestionCategory).all()

    question = db_session.query(Question).filter_by(id=question_id).first()

    anwers = db_session.query(AnswerOption).filter_by(spørsmål_id=question_id).all()

    edited_answers = []

    new_answers = []

    if request.method == "POST":

        print(request.form)

        answer_inputs = [key for key in request.form.keys() if key.startswith("answer-")]

        for answer_input in answer_inputs:

            answer_id = int(answer_input.split("-")[-1])

            edited_answers.append({"id": answer_id, "svar": request.form.get(answer_input), "korrekt": f"correct-{answer_id}" in request.form})

        i = 1

        while f"new-answer-{i}" in request.form:

            new_answers.append({"svar": request.form.get(f"new-answer-{i}"), "korrekt": f"new-correct-{i}" in request.form})

            i += 1

        try:

            if len(edited_answers) + len(new_answers) == 1:

                flash("Spørsmål må ha minst to svaralternativer. Eneste unntak er et type spørsmål (essay).", category="error")

                return render_template("quiz/edit_question.html", answers=anwers, new_answers=new_answers, categories=categories, question=request.form.get("question"), category_id=request.form.get("category-select"), question_id=question_id)

            if (edited_answers or new_answers) and not any([answer["korrekt"] for answer in edited_answers]) and not any([answer["korrekt"] for answer in new_answers]):

                flash("Spørsmål må ha minst ett korrekt svaralternativ.", category="error")

                return render_template("quiz/edit_question.html", answers=anwers, new_answers=new_answers, categories=categories, question=request.form.get("question"), category_id=request.form.get("category-select"), question_id=question_id)

            question.spørsmål = request.form.get("question")

            question.kategori_id = request.form.get("category-select")

            db_session.commit()

            for answer in edited_answers:

                answer_option = db_session.query(AnswerOption).filter_by(id=answer["id"]).first()

                answer_option.svar = answer["svar"]

                answer_option.korrekt = answer["korrekt"]

                db_session.commit()

            for answer in new_answers:

                answer_option = AnswerOption(spørsmål_id=question.id, svar=answer["svar"], korrekt=answer["korrekt"])

                db_session.add(answer_option)

                db_session.commit()

            flash(f"Spørsmålet '{question.spørsmål}' er nå endret.", category="success")

            return redirect(url_for("admin.admin_profile"))

        except Exception as exception:

            flash(f"{type(exception).__name__}: {exception}", category="error")

            return render_template("quiz/edit_question.html", answers=anwers, new_answers=new_answers, categories=categories, question=request.form.get("question"), category_id=request.form.get("category-select"), question_id=question_id)

    return render_template("quiz/edit_question.html", answers=anwers, new_answers=new_answers, categories=categories, question=question.spørsmål, category_id=question.kategori_id, question_id=question.id)


@quiz.route("/add-answer", methods=["POST"])
@login_required
def add_answer():

    categories = db_session.query(QuestionCategory).all()

    answers = []

    i = 1

    while f"answer-{i}" in request.form:

        answers.append({'svar': request.form.get(f"answer-{i}"), 'korrekt': request.form.get(f"correct-{i}") == 'True'})

        i += 1

    answers.append({'svar': request.form.get("new-answer"), 'korrekt': 'new-correct' in request.form})

    return render_template("quiz/add_question.html", answers=answers, categories=categories, question=None, category_id=None)


@quiz.route("/add-answer-for-edit/<int:question_id>", methods=["POST"])
@login_required
def add_answer_for_edit(question_id):

    categories = db_session.query(QuestionCategory).all()

    question = db_session.query(Question).filter_by(id=question_id).first()

    answers = db_session.query(AnswerOption).filter_by(spørsmål_id=question_id).all()

    new_answers = []

    i = 1

    while f"new-answer-{i}" in request.form:

        new_answers.append({'svar': request.form.get(f"new-answer-{i}"), 'korrekt': request.form.get(f"new-correct-{i}") == 'True'})

        i += 1

    new_answers.append({'svar': request.form.get("new-answer"), 'korrekt': 'new-correct' in request.form})

    return render_template("quiz/edit_question.html", answers=answers, new_answers=new_answers, categories=categories, question=question.spørsmål, category_id=question.kategori_id, question_id=question_id)


@quiz.route("/remove-answer/<int:answer_id>")
@login_required
def remove_answer(answer_id):

    awnser = db_session.query(AnswerOption).filter_by(id=answer_id).first()

    answers = [ao for ao in db_session.query(AnswerOption).filter_by(spørsmål_id=awnser.spørsmål_id).all() if ao.id != answer_id]

    categories = db_session.query(QuestionCategory).all()

    question = db_session.query(Question).filter_by(id=awnser.spørsmål_id).first()

    if len(answers) == 1:

        flash("Spørsmål må ha minst to svaralternativer. Eneste unntak er et type spørsmål (essay).", category="error")

        return render_template("quiz/edit_question.html", answers=answers, categories=categories, question=question.spørsmål, category_id=question.kategori_id, question_id=question.id)

    if answers and not any([answer.korrekt for answer in answers]):

        flash("Spørsmål må ha minst ett korrekt svaralternativ.", category="error")

        return render_template("quiz/edit_question.html", answers=answers, categories=categories, question=question.spørsmål, category_id=question.kategori_id, question_id=question.id)

    db_session.delete(awnser)

    db_session.commit()

    return render_template("quiz/edit_question.html", answers=answers, categories=categories, question=question.spørsmål, category_id=question.kategori_id, question_id=question.id)


@quiz.route("/add-category", methods=["POST"])
@login_required
def add_category():

    category = QuestionCategory(navn=request.form.get("category_name"))

    db_session.add(category)

    db_session.commit()

    flash(f"Kategorien '{category.navn}' er nå lagt til.", category="success")

    return redirect(url_for("admin.admin_profile"))
