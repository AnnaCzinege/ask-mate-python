import database_common


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
        SELECT * FROM questions;
    """)
    question_details = cursor.fetchall()
    return question_details


@database_common.connection_handler
def get_question_id_title(cursor):
    cursor.execute("""
        SELECT id, title FROM questions;
    """)
    question = cursor.fetchall()
    return question

@database_common.connection_handler
def add_new_question(cursor, add_dict):
    title = add_dict['title']
    message = add_dict['message']
    cursor.execute("""
                    INSERT INTO questions
                    VALUES (%(title)s, %(message)s);
                    """,
                   {'title': title, 'message': message})


@database_common.connection_handler
def edit_question(cursor, edit_dict):
    new_title = edit_dict['title']
    question_id = edit_dict['id']
    new_message = edit_dict['message']
    cursor.execute("""
                    UPDATE questions
                    SET title = %(new_title)s,
                    message = %(new_message)s
                    WHERE id = %(question_id)s;
                    """,
                   {'id': question_id, 'title': new_title, 'message': new_message})


@database_common.connection_handler
def list_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answers
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_question_details_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM questions
                    WHERE id = %(question_id)s
                    """, {'question_id': question_id})
    return cursor.fetchall()

