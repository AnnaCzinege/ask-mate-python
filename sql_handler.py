import database_common


@database_common.connection_handler
def list_all_questions(cursor):
    cursor.execute("""
                    SELECT id, title
                    FROM questions;
                    """)
    question_table = cursor.fetchall()
    return question_table


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
de