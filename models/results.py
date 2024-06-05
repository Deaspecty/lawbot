import json
from models.question import get_questions, get_questions


def find_result(cursor, combination: list, id: int):
    questions = get_questions(cursor, id)
    if len(combination) == len(questions):
        text = f"Ответы на вопросы из категории {id}: \n"
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


def create_all_combinations(cursor):
    for id in [1, 2, 3]:
        questions = get_questions(cursor, id, "bool")
        for combination in generate_bool_arrays(len(questions)):
            json_combination = {}
            if len(combination) == len(questions):
                for i in range(len(questions)):
                    json_combination.update({questions[i][1]: combination[i]})
                json_combination = json.dumps(json_combination)

                cursor.execute("SELECT * FROM results WHERE combination = %s", (json_combination,))
                results = cursor.fetchone()
                if results is not None and results[2] is not None:
                    continue
                else:
                    result_str = f"Ответ из категории {id}, " \
                                 f"исходя из ответов {'-'.join(['Да' if i else 'Нет' for i in combination])}"
                    cursor.execute("INSERT INTO results(combination, result) VALUES (%s, %s)",
                                   (json_combination, result_str))


