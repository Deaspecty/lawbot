def get_all_questions(cursor):
    cursor.execute("SELECT * FROM questions")
    return cursor.fetchall()


def get_questions_by_category(cursor, category_id: int):
    cursor.execute("SELECT * FROM questions WHERE category_id = %s", (category_id,))
    return cursor.fetchall()