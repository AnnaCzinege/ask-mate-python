import database_common
from psycopg2 import sql


def normalize_output_single_row(normalize_me):  # Creates a simple dictionary
    dump_dictionary = {}
    for row in normalize_me:
        for key, value in row.items():
            dump_dictionary[key] = value
    return dump_dictionary


def normalize_output_multiple_rows(normalize_me):  # Creates dictionaries in a list
    normalized_output = []
    for row in normalize_me:
        dump_dictionary = {}
        for key, value in row.items():
            dump_dictionary[key] = value
        normalized_output.append(dump_dictionary)
    return normalized_output


@database_common.connection_handler
def get_questions(cursor):
    cursor.execute("""
        SELECT * FROM questions
            ORDER BY id;
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
    user_id = add_dict['user_id']
    title = add_dict['title']
    message = add_dict['message']
    cursor.execute("""
                    INSERT INTO questions (user_id, title, message)
                    VALUES (%(user_id)s, %(title)s, %(message)s);
                    """,
                   {'user_id': user_id,'title': title, 'message': message})


@database_common.connection_handler
def add_new_answer(cursor, add_dict):
    question_id = add_dict['id']
    user_id = add_dict['user_id']
    question_message = add_dict['message']
    cursor.execute("""
                    INSERT INTO answers (question_id, user_id, message)
                    VALUES (%(id)s, %(user_id)s, %(message)s);
                    """,
                   {'id': question_id, 'user_id': user_id, 'message': question_message})


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
                   {'question_id': question_id, 'new_title': new_title, 'new_message': new_message})


@database_common.connection_handler
def list_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answers
                    WHERE question_id = %(question_id)s
                    ORDER BY id;
                    """, {'question_id': question_id})
    answers = cursor.fetchall()
    answers = normalize_output_multiple_rows(answers)
    return answers


@database_common.connection_handler
def get_answer_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT message, question_id, id FROM answers
                    WHERE id = %(answer_id)s
                    """,
                   {'answer_id': answer_id})
    answer = cursor.fetchall()
    answer = normalize_output_single_row(answer)
    return answer


@database_common.connection_handler
def get_question_details_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM questions
                    WHERE id = %(question_id)s
                    """, {'question_id': question_id})
    question_details = cursor.fetchall()
    question_details = normalize_output_single_row(question_details)
    return question_details


@database_common.connection_handler
def delete_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT id FROM answers
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})
    answer_id_list = [little_dict['id'] for little_dict in normalize_output_multiple_rows(cursor.fetchall())]
    for item in answer_id_list:
        cursor.execute("""
                        DELETE FROM answer_comments
                        WHERE answer_id = %(item)s
                        """, {'item': item})

    cursor.execute("""
                    DELETE FROM questions
                    WHERE id = %(question_id)s;
                    
                    DELETE FROM answers
                    WHERE question_id = %(question_id)s;
                    
                    DELETE FROM question_comments
                    WHERE question_id = %(question_id)s;                   
                    """, {'question_id': question_id})


@database_common.connection_handler
def sort_questions(cursor, direction):
    if direction == 'asc':
        cursor.execute("""
                        SELECT id, title, user_id AS userid FROM questions
                        ORDER BY title;
                        """)
        return normalize_output_multiple_rows(cursor.fetchall())
    else:
        cursor.execute("""
                        SELECT id, title, user_id AS userid FROM questions
                        ORDER BY title DESC;
                        """)
        return normalize_output_multiple_rows(cursor.fetchall())


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answers
                    WHERE id = %(answer_id)s
                    """, {'answer_id': answer_id})


@database_common.connection_handler
def edit_answer(cursor, add_dict):
    answer_id = add_dict['answer_id']
    message = add_dict['message']
    cursor.execute("""
                    UPDATE answers
                    SET message = %(message)s
                    WHERE id = %(answer_id)s
                    """, {'message': message, 'answer_id': answer_id})


@database_common.connection_handler
def add_question_comment(cursor, add_dict):
    user_id = add_dict['user_id']
    question_id = add_dict['question_id']
    comment = add_dict['comment']
    cursor.execute("""
                    INSERT INTO question_comments (user_id, question_id, comment)
                    VALUES (%(user_id)s, %(question_id)s, %(comment)s);
                    """, {'user_id': user_id, 'question_id': question_id, 'comment': comment})


@database_common.connection_handler
def delete_question_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM question_comments
                    WHERE id = %(comment_id)s;
                    """, {'comment_id': comment_id})


@database_common.connection_handler
def get_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM question_comments
                    WHERE id = %(comment_id)s
                    """, {'comment_id': comment_id})
    return normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def get_answer_comment(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM answer_comments
                    WHERE id = %(comment_id)s
                    """,
                   {'comment_id': comment_id})
    return normalize_output_single_row(cursor.fetchall())


@database_common.connection_handler
def edit_question_comment(cursor, add_dict):
    comment_id = add_dict['comment_id']
    comment = add_dict['comment']
    cursor.execute("""
                    UPDATE question_comments
                    SET comment = %(comment)s
                    WHERE id = %(comment_id)s  
                    """, {'comment_id': comment_id, 'comment': comment})


@database_common.connection_handler
def count_comments_for_question(cursor, question_id_):
    cursor.execute("""
                    SELECT COUNT(question_id)
                    FROM question_comments
                    WHERE question_id = %(question_id_)s;
                    """, {'question_id_': question_id_})
    comments = cursor.fetchone()
    return comments['count']


@database_common.connection_handler
def count_comments_for_answer(cursor, answer_id_):
    cursor.execute("""
                    SELECT COUNT(answer_id)
                    FROM answer_comments
                    WHERE answer_id = %(answer_id_)s;
                    """, {'answer_id_': answer_id_})
    comments = cursor.fetchone()
    return comments['count']


@database_common.connection_handler
def add_answer_comment(cursor, add_dict):
    user_id = add_dict['user_id']
    answer_id = add_dict['answer_id']
    comment = add_dict['comment']
    cursor.execute("""
                    INSERT INTO answer_comments (user_id, answer_id, comment)
                    VALUES (%(user_id)s, %(answer_id)s, %(comment)s)
                    """, {'user_id': user_id, 'answer_id': answer_id, 'comment': comment})


@database_common.connection_handler
def delete_answer_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE FROM answer_comments
                    WHERE id = %(comment_id)s
                    """, {'comment_id': comment_id})


@database_common.connection_handler
def edit_answer_comment(cursor, add_dict):
    comment_id = add_dict['comment_id']
    comment = add_dict['comment']
    cursor.execute("""
                    UPDATE answer_comments 
                    SET comment = %(comment)s
                    WHERE id = %(comment_id)s
                    """, {'comment_id': comment_id, 'comment': comment})


@database_common.connection_handler
def get_answer_comments(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer_comments
                    WHERE answer_id = %(answer_id)s
                    ORDER BY id
                    """, {'answer_id': answer_id})
    return normalize_output_multiple_rows(cursor.fetchall())


@database_common.connection_handler
def display_latest_question(cursor):
    cursor.execute("""
                    SELECT title, id FROM questions
                    ORDER BY id DESC 
                    LIMIT 1;
                    """)
    latest_question = cursor.fetchall()
    latest_question = normalize_output_single_row(latest_question)
    return latest_question


@database_common.connection_handler
def search_by_phrase(cursor, phrase):
    phrase = phrase.lower()
    cursor.execute(sql.SQL("""
                    SELECT id, title, message FROM questions
                    WHERE LOWER(title) LIKE '%{match}%' OR LOWER(message) LIKE '%{match}%'
                    ORDER BY id DESC
                    """).format(match=sql.SQL(phrase)))
    match = cursor.fetchall()
    match = normalize_output_multiple_rows(match)
    match_matrix = [dict_['message'].split(' ') for dict_ in match]
    for index, word_list in enumerate(match_matrix):
        for word_index, word in enumerate(word_list):
            if phrase.lower() in word.lower():
                word_list[word_index] = f"<mark>{word}</mark>"
                match[index]['message'] = " ".join(match_matrix[index])
    return match


@database_common.connection_handler
def search_sort(cursor, direction, search_phrase):
    search_phrase = search_phrase.lower()
    if direction == 'asc':
        cursor.execute(sql.SQL("""
                        SELECT id, title FROM questions
                        WHERE LOWER(title) LIKE '%{match}%' OR LOWER(message) LIKE '%{match}%'
                        ORDER BY title
                        """).format(match=sql.SQL(search_phrase)))
        return normalize_output_multiple_rows(cursor.fetchall())
    else:
        cursor.execute(sql.SQL("""
                        SELECT id, title FROM questions
                         WHERE LOWER(title) LIKE '%{match}%' OR LOWER(message) LIKE '%{match}%'
                        ORDER BY title DESC;
                        """).format(match=sql.SQL(search_phrase)))
        return normalize_output_multiple_rows(cursor.fetchall())


@database_common.connection_handler
def get_question_comments(cursor, question_id):
    cursor.execute("""
                    SELECT comment, id FROM question_comments
                    WHERE question_id = %(question_id)s
                    ORDER BY id;
                    """, {'question_id': question_id})
    return normalize_output_multiple_rows(cursor.fetchall())
