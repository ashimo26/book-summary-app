# quiz/quiz_state.py
_current_answer = None

def set_current_answer(answer, options):
    global _current_answer
    if answer.upper() in ["A", "B", "C", "D"]:
        idx = ord(answer.upper()) - ord("A")
        _current_answer = options[idx] if idx < len(options) else options[0]
    else:
        _current_answer = answer

def get_current_answer():
    return _current_answer