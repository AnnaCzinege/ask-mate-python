import database_common
import sql_handler
from psycopg2 import sql


@database_common.connection_handler
def get_usernames(cursor):
    cursor.execute("""
                    SELECT username FROM users
                    """)
    return [dict_['username'] for dict_ in sql_handler.normalize_output_multiple_rows(cursor.fetchall())]


@database_common.connection_handler
def add_user_info(cursor, info_list):
    username = info_list[0]
    password = info_list[1]
    cursor.execute(sql.SQL("""
                            INSERT into users (username, password)
                            VALUES ('{username}', '{password}')
                            """).format(username=sql.SQL(username), password=sql.SQL(password)))


@database_common.connection_handler
def get_hashed_pass(cursor, username):
    cursor.execute(sql.SQL("""
                                SELECT password FROM users
                                WHERE username = '{username}'
                                """).format(username=sql.SQL(username)))
    return sql_handler.normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def get_userid_by_username(cursor, username):
    cursor.execute(sql.SQL("""
                    SELECT id FROM users
                    WHERE username = '{username}'
                    """).format(username=sql.SQL(username)))
    return sql_handler.normalize_output_single_row(cursor.fetchall())

@database_common.connection_handler
def get_username_by_id(cursor, userid):
    cursor.execute(sql.SQL("""
                    SELECT username FROM users
                    WHERE id = '{userid}'
                    """).format(username=sql.SQL(userid)))
    return sql_handler.normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def get_question_id_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT id FROM questions
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return sql_handler.normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def get_answer_id_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT id FROM answers
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return sql_handler.normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def list_questions_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT id, user_id, title FROM questions
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def list_answers_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT questions.title, answers.message, COUNT(answers.message) as "All answers", question_id FROM answers
                    INNER JOIN questions ON question_id = questions.id
                    WHERE answers.user_id = %(user_id)s
                    GROUP BY questions.title, question_id, answers.message
                    """, {'user_id': user_id})
    return cursor.fetchall()