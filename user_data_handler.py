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
def count_answers_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT questions.title, COUNT(answers.message) as "count_answers", question_id 
                    FROM answers
                    INNER JOIN questions ON question_id = questions.id
                    WHERE answers.user_id = %(user_id)s
                    GROUP BY question_id, questions.title
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def list_answers_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT *
                    FROM answers
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def count_comments_on_question_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT questions.title, COUNT(question_comments.comment) as "count_comments", question_id 
                    FROM question_comments
                    INNER JOIN questions ON question_id = questions.id
                    WHERE question_comments.user_id = %(user_id)s
                    GROUP BY question_id, questions.title
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def list_comments_on_questions_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT *
                    FROM question_comments
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return cursor.fetchall()

@database_common.connection_handler
def count_comments_on_answer_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT answers.message, COUNT(answer_comments.comment) as "count_comments", 
                    answers.id, answers.question_id
                    FROM answer_comments
                    INNER JOIN answers ON answer_comments.answer_id = answers.id
                    WHERE answer_comments.user_id = %(user_id)s
                    GROUP BY answers.message, answers.id, answers.question_id
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def list_comments_on_answers_by_user_id(cursor, user_id):
    cursor.execute("""
                    SELECT *
                    FROM answer_comments
                    WHERE user_id = %(user_id)s
                    """, {'user_id': user_id})
    return cursor.fetchall()


@database_common.connection_handler
def get_user_info(cursor):
    cursor.execute("""
                    SELECT users.id, users.username,
                     users.date, count(distinct questions.id) as count,
                     count(distinct answers.id) as count_answer,
                     count(distinct question_comments.id) as count_q_c,
                     count(distinct answer_comments.id) as count_a_c
                    FROM users
                    LEFT JOIN questions ON users.id = questions.user_id
                    LEFT JOIN answers ON users.id = answers.user_id
                    LEFT JOIN question_comments ON users.id = question_comments.user_id
                    LEFT JOIN answer_comments ON users.id = answer_comments.user_id
                    GROUP BY users.id
                    """)
    return sql_handler.normalize_output_multiple_rows(cursor.fetchall())

@database_common.connection_handler
def get_user_role(cursor, user_id):
    cursor.execute("""
                    SELECT role 
                    FROM users
                    WHERE id = %(user_id)s
                    """, {'user_id': user_id})
    return sql_handler.normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def get_question_num_user(cursor):
    cursor.execute("""
                    SELECT user_id, count(id) as count_questions
                    FROM questions
                    GROUP BY user_id
                    """)
    return sql_handler.normalize_output_multiple_rows(cursor.fetchall())

@database_common.connection_handler
def get_author_of_answer_by_questionid(cursor, questionid):
    cursor.execute(sql.SQL("""
                    SELECT answers.id, users.username FROM answers
                    INNER JOIN users ON answers.user_id = users.id
                    WHERE answers.question_id = '{questionid}'
                    """).format(questionid=sql.SQL(questionid)))
    return sql_handler.normalize_output_multiple_rows(cursor.fetchall())



@database_common.connection_handler
def mark_answer_as_accepted(cursor, answer_id, question_id):
    cursor.execute("""
                    UPDATE answers
                    SET accepted = FALSE
                    WHERE accepted = TRUE and question_id = %(question_id)s;
                    
                    UPDATE answers
                    SET accepted = TRUE
                    WHERE id = %(answer_id)s;
                    """, {'answer_id': answer_id,
                          'question_id': question_id})
