
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(user_id, current_question, user_answer, session):
    # Assume session is a dictionary that stores users' states and answers
    if user_id not in session:
        session[user_id] = {'answers': {}, 'current_question_index': 0}

    # Validate the answer (this part will depend on how validation is defined in your application)
    if is_valid_answer(current_question, user_answer):
        session[user_id]['answers'][current_question['id']] = user_answer
        return True
    else:
        return False

def is_valid_answer(current_question, user_answer):
    # Implement your validation logic here
    # For example, checking if the answer is among the possible choices
    return user_answer in current_question['choices']


def get_next_question(user_id, questions, session):
    if user_id not in session:
        session[user_id] = {'answers': {}, 'current_question_index': 0}

    current_index = session[user_id]['current_question_index']
    
    if current_index < len(questions):
        next_question = questions[current_index]
        session[user_id]['current_question_index'] += 1
        return next_question
    else:
        return None  # No more questions left

def generate_final_response(user_id, questions, session):
    if user_id not in session:
        return "Error: No session found for the user."

    answers = session[user_id]['answers']
    score = 0
    total_questions = len(questions)
    
    for question in questions:
        correct_answer = question['correct_answer']
        user_answer = answers.get(question['id'])
        if user_answer == correct_answer:
            score += 1

 
    return "dummy result"
