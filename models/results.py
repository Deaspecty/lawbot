import json
from models.question import get_questions, get_questions


def find_result(cursor, combination: list, id: int, name: str):
    questions = get_questions(cursor, id)
    if len(combination) == len(questions):
        text = f"Ответы на вопросы из категории {name}: \n"
        for i in range(len(questions)):
            if type(combination[i]) == bool:
                text += f"{questions[i][1]} - {'Да' if combination[i] else 'Нет'}\n"
            else:
                text += f"{questions[i][1]} - {combination[i]}\n"
        return text


def generate_bool_arrays(n):
    if n == 0:
        return [[]]
    else:
        smaller_arrays = generate_bool_arrays(n - 1)
        result = []
        for array in smaller_arrays:
            result.append(array + [False])
            result.append(array + [True])
        return result