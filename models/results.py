import json
from models.question import get_questions_by_category, get_all_questions


def find_result(cursor, combination: list[bool], id: int):
    questions = get_questions_by_category(cursor, id)
    json_combination = {}
    if len(combination) == len(questions):
        for i in range(len(questions)):
            json_combination.update({questions[i][1]: combination[i]})
        json_combination = json.dumps(json_combination)

        cursor.execute("SELECT * FROM results WHERE combination = %s", (json_combination,))
        results = cursor.fetchone()
        if results is not None and results[2] is not None:
            return results[2]
        else:
            cursor.execute("INSERT INTO results(combination) VALUES (%s)", (json_combination,))
            return "COMBINATION NOT FOUND!"


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
        for combination in generate_bool_arrays(3):
            questions = get_questions_by_category(cursor, id)
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


