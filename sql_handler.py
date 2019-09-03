import database_common


def normalize_output_single_row(brainfuck):  # Creates a simple dictionary
    dump_dictionary = {}
    for row in brainfuck:
        for key, value in row.items():
            dump_dictionary[key] = value
    return dump_dictionary


def normalize_output_multiple_rows(brainfuck):  # Creates dictionaries in a list
    normalized_output = []
    for row in brainfuck:
        dump_dictionary = {}
        for key, value in row.items():
            dump_dictionary[key] = value
        normalized_output.append(dump_dictionary)
    return normalized_output


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
                    INSERT INTO questions (title,message)
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
                   {'question_id': question_id, 'new_title': new_title, 'new_message': new_message})


@database_common.connection_handler
def list_answers_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answers
                    WHERE question_id = %(question_id)s
                    """, {'question_id': question_id})
    answers = cursor.fetchall()
    answers = normalize_output_multiple_rows(answers)
    return answers


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
                    DELETE FROM questions
                    WHERE id = %(question_id)s
                    """, {'question_id': question_id})


@database_common.connection_handler
def sort_questions(cursor, direction):
    if direction == 'asc':
        cursor.execute("""
                        SELECT id, title FROM questions
                        ORDER BY title;
                        """)
        return normalize_output_multiple_rows(cursor.fetchall())
    else:
        cursor.execute("""
                        SELECT id, title FROM questions
                        ORDER BY title DESC;
                        """)
        return normalize_output_multiple_rows(cursor.fetchall())
