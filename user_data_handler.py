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
