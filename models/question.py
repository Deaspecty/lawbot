def get_questions(cursor, category_id=None, q_type=None):
    if category_id is not None and q_type is not None:
        cursor.execute("SELECT * FROM questions WHERE category_id = %s and type=%s", (category_id, q_type))
    elif category_id is not None:
        cursor.execute("SELECT * FROM questions WHERE category_id = %s", (category_id,))
    else:
        cursor.execute("SELECT * FROM questions")
    questions = cursor.fetchall()
    return sorted(questions, key=lambda que: que[0])