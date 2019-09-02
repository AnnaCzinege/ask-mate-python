import database_common


@database_common.connection_handler
def list_all_questions(cursor):
    cursor.execute("""
                    SELECT title
                    FROM questions
                    """)
    question_table = cursor.fetchall()
    return question_table
