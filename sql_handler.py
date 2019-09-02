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
