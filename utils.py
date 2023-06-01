def parse_quiz_form_data(questions, form):
    
    answers = {}
    
    for question in questions:

        correct, particulary_correct, incorrect = True, False, False
        
        answer = {
            "answers": {}
        }
        
        text_answer = None

        if str(question["id"]) in form:

            answers_list = form.getlist(str(question["id"]))

            for answer_str in answers_list:
                
                answer_splitted = answer_str.split(' ')

                answer_correct = bool(int(answer_splitted[1]))

                answer["answers"][int(answer_splitted[0])] = {'correct': answer_correct}

                correct = correct and answer_correct
                particulary_correct = particulary_correct or answer_correct
                incorrect = incorrect or answer_correct

        elif f"text-answer-{question['id']}" in form:
            text_answer = form[f"text-answer-{question['id']}"]

        answered = bool(answer["answers"])

        answer["correct"], answer["particulary_correct"], answer["incorrect"], answer['not_answered'] = answered and correct, answered and not correct and particulary_correct, answered and not incorrect, not answered

        answer["text_answer"] = text_answer if text_answer and not text_answer.isspace() else None

        answers[question["id"]] = answer
        
    return answers
