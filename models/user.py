def save_user(cursor, phone_number, name, id):
    cursor.execute("UPDATE users SET fullname=%s, phone_number=%s WHERE id=%s", (phone_number, name, id))
    cursor.close()