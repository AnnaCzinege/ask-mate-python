import database_common


@database_common.connection_handler
def list_all_questions(cursor):
    cursor.execute("""
                    SELECT id, title
                    FROM questions
                    """)
    question_table = cursor.fetchall()
    return question_table
