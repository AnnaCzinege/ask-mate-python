from flask import Flask, request, render_template, redirect, url_for, session, escape
import sql_handler
import user_data_handler
import hash

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.form['username'].lower()
    password = request.form['password']
    if username in user_data_handler.get_usernames() and hash.verify_pass(password, user_data_handler.get_hashed_pass(username)['password']):
        session['username'] = username
        user_id = user_data_handler.get_userid_by_username(username)
        user_id = user_id['id']
        session['user_id'] = user_id
        return redirect('/')
    return redirect('/')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    username = request.form['username'].lower()
    password = hash.hash_pass(request.form['password'])
    if username in user_data_handler.get_usernames():
        return redirect('/')
    user_data_handler.add_user_info([username, password])
    return redirect('/')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')


@app.route('/<user_name>')
def view_profile(user_name):
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_role = None
    user = user_name
    user_id = user_data_handler.get_userid_by_username(user)['id']
    user_questions = user_data_handler.list_questions_by_user_id(user_id)
    user_answers_count = user_data_handler.count_answers_by_user_id(user_id)
    user_answers = user_data_handler.list_answers_by_user_id(user_id)
    user_comments_count_question = user_data_handler.count_comments_on_question_by_user_id(user_id)
    user_comments_on_questions = user_data_handler.list_comments_on_questions_by_user_id(user_id)
    user_comments_count_answer = user_data_handler.count_comments_on_answer_by_user_id(user_id)
    user_comments_on_answers = user_data_handler.list_comments_on_answers_by_user_id(user_id)
    return render_template('user_profile.html', user_name=user_name, user=user,
                           user_questions=user_questions, user_answers=user_answers,
                           logged_in_as=session_name,
                           user_answers_count=user_answers_count,
                           user_id=user_id, user_role=user_role,
                           user_comments_count_question=user_comments_count_question,
                           user_comments_on_questions=user_comments_on_questions,
                           user_comments_count_answer=user_comments_count_answer,
                           user_comments_on_answers=user_comments_on_answers)


@app.route('/user-details')
def view_user_details():
    user_name = escape(session['username'])
    user_infos = user_data_handler.get_user_info()
    return render_template('all_user_details.html',
                           user_infos=user_infos,
                           logged_in_as=f"You are logged in as {escape(session['username'])}")



@app.route("/", methods=['GET', 'POST'])
@app.route("/<int:num>")
@app.route("/show/<int:id_>", methods=["GET", "POST"])
@app.route("/list/<string:id_>", methods=["GET", "POST"])
def route_list(id_=None, num=None):
    user_id = 0
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None

    id_title = sql_handler.get_question_id_title()
    if request.method == "POST":
        found_search = sql_handler.search_by_phrase(request.form['search_phrase'])
        dir_ = request.args.get("dir_")
        return render_template("search.html", found_search=found_search, dir_=dir_,
                               search_phrase=request.form['search_phrase'],
                               logged_in_as=session_name,
                               user_name=user_name,
                               user_role=user_role)
    if num is not None:
        dir_ = request.args.get("dir_")
        id_title = sql_handler.sort_questions(dir_)
        user_id = int(escape(session['user_id']))
        return render_template("list.html", id_title=id_title, dir_=dir_, logged_in_as=session_name,
                               user_name=user_name, error_message=None, user_id=user_id, user_role=user_role)
    return render_template("list.html", id_title=id_title, logged_in_as=session_name, user_name=user_name,
                           error_message=None, user_id=user_id, user_role=user_role)


@app.route("/delete/<int:id_>", methods=["POST", "GET"])
def route_delete(id_=None):
    # When you click on delete action button
    if request.method == "POST":
        sql_handler.delete_question_by_id(id_)
        return redirect("/")

    # This message will be shown when you try to delete something by hand in the URL
    return "Azt te csak szeretnéd! :)"


@app.route("/add", methods=["POST", "GET"])
def route_add():
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        return redirect('/')
    # When finished adding
    if request.method == "POST":
        if 'username' in session:
            username = escape(session['username'])
            user_id = user_data_handler.get_userid_by_username(username)
            user_id = user_id['id']
            row = {'user_id': str(user_id), 'title': str(request.form["title"]), 'message': str(request.form["message"])}
            sql_handler.add_new_question(row)
            return redirect("/")
        else:
            user_name = None
            user_id = int(escape(session['user_id']))
            session_name = 'You are not logged in'
            dir_ = request.args.get("dir_")
            id_title = sql_handler.sort_questions(dir_)
            error_message = 'You have to log in first!'
            return render_template("list.html", id_title=id_title, logged_in_as=session_name, user_name=user_name,
                                   error_message=error_message, user_id=user_id, user_role=user_role)

    # When someone clicks on add new question button
    return render_template("add_edit.html", id_=None, title='Add new question',
                           logged_in_as=session_name, user_name=user_name, user_role=user_role)


@app.route("/edit", methods=["POST", "GET"])
@app.route("/edit/<id_>", methods=["POST", "GET"])
def route_edit(id_=None):
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None
    # When you finished updating the question
    if request.method == "POST" and id_ is not None:
        user_id = int(escape(session['user_id']))
        questionuserid = sql_handler.get_questionuserid_by_questionid(id_)
        questionuserid = questionuserid['user_id']
        if user_id == questionuserid:
            updated_row = {'id': request.form["id_"], 'title': request.form["title"], 'message': request.form["message"]}
            sql_handler.edit_question(updated_row)
            return redirect("/")
        else:
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # When you click the edit action button
    if id_ is not None:
        question = sql_handler.get_question_details_by_id(id_)
        return render_template("add_edit.html", id_=question['id'],
                               row_title=question['title'],
                               row_message=question['message'],
                               title="Edit question",
                               logged_in_as=session_name,
                               user_name=user_name,
                               user_role=user_role)


@app.route("/question_details/<id_>", methods=['GET', 'POST'])
@app.route("/question_details/<id_>/<answer_id>/<answer_message>", methods=["GET", "POST"])
def show_question_details(id_=None, answer_id=None, answer_message=''):
    user_id = 0
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None

    question = sql_handler.get_question_details_by_id(id_)
    answers = sql_handler.list_answers_by_question_id(id_)
    comment_number = sql_handler.count_comments_for_question(id_)
    list_of_comment_numbers_on_answers = []
    question_username = sql_handler.show_username_at_question(id_)
    authors_of_answers = user_data_handler.get_author_of_answer_by_questionid(id_)
    authors_of_answers = [element['username'] for element in authors_of_answers]

    if answer_id is not None:
        where_url = url_for("edit_answer", answer_id=answer_id)
    else:
        where_url = url_for("show_question_details", id_=id_)

    for item in answers:
        answer_id = item['id']
        num_of_comments = sql_handler.count_comments_for_answer(answer_id)
        list_of_comment_numbers_on_answers.append(num_of_comments)

    if request.method == "POST":  # When you submit an answer

        user_id = user_data_handler.get_userid_by_username(user_name)
        user_id = user_id['id']
        answer = {'id': id_, 'user_id': user_id, 'message': str(request.form['answer'])}
        sql_handler.add_new_answer(answer)
        return redirect(url_for('show_question_details', id_=id_))

    return render_template("question_details.html",
                           row_user_id=question['user_id'],
                           row_title=question['title'],
                           row_question=question['message'],
                           answer_list=answers,
                           where_url=where_url,
                           comment_number=comment_number,
                           comment_number_answer=list_of_comment_numbers_on_answers,
                           id_=id_,
                           answer_message=answer_message,
                           logged_in_as=session_name,
                           user_name=user_name,
                           user_role=user_role,
                           user_id=user_id,
                           question_username=question_username['username'],
                           authors_of_answers=authors_of_answers
                           )


@app.route('/edit-answer', methods=["POST", "GET"])
@app.route('/edit-answer/<answer_id>', methods=["POST", "GET"])
def edit_answer(answer_id):
    answer = sql_handler.get_answer_by_answer_id(answer_id)
    question_id = answer['question_id']
    if request.method == 'POST':
        updated_answer = {'answer_id': answer_id, 'message': request.form['answer']}
        sql_handler.edit_answer(updated_answer)
        return redirect(f"/question_details/{question_id}")
    answer_message = answer['message']
    return redirect(f'/question_details/{question_id}/{answer_id}/{answer_message}')


@app.route("/delete-answer/<answer_id>", methods=["POST", "GET"])
def delete_answer(answer_id):
    answer = sql_handler.get_answer_by_answer_id(answer_id)
    question_id = answer['question_id']
    if request.method == "POST":
        sql_handler.delete_answer(answer_id)
        return redirect(f"/question_details/{question_id}")


@app.route('/show-answer-comments/<question_id>/<answer_id>', methods=["POST", "GET"])
@app.route('/show-answer-comments/<qucomment_idestion_id>/<answer_id>/<comment_id>/<comment_message>', methods=["POST", "GET"])
def show_answer_comments(question_id, answer_id, comment_id=None, comment_message=''):
    user_id = 0
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None
    if request.method == "POST":
        user_id = user_data_handler.get_userid_by_username(user_name)
        user_id = user_id['id']
        add_dict = {'answer_id': answer_id, 'user_id': user_id, 'comment': request.form['comment']}
        sql_handler.add_answer_comment(add_dict)
    if comment_id is not None:
        where_url = url_for('edit_answer_comment', question_id=question_id, answer_id=answer_id, comment_id=comment_id)
    else:
        where_url = url_for('show_answer_comments', question_id=question_id, answer_id=answer_id)
    comments = sql_handler.get_answer_comments(answer_id)
    answer = sql_handler.get_answer_by_answer_id(answer_id)
    return render_template('comments.html',
                           comments=comments,
                           answer=answer['message'],
                           question_id=question_id,
                           back_url=url_for("show_question_details", id_=question_id),
                           comment_id=comment_id,
                           comment_to_edit=comment_message,
                           where_url=where_url,
                           logged_in_as=session_name,
                           user_name=user_name,
                           user_id=user_id,
                           user_role=user_role)


@app.route("/delete-answer-comment/<question_id>/<answer_id>/<comment_id>", methods=['GET', 'POST'])
def delete_answer_comment(question_id, answer_id, comment_id):
    sql_handler.delete_answer_comment(comment_id)
    return redirect(f'/show-answer-comments/{question_id}/{answer_id}')


@app.route("/show-comments/<id_>/<comment_id>/<comment_message>")
@app.route("/show-comments/<id_>", methods=['GET', 'POST'])
def show_question_comments(id_, comment_id=None, comment_message=''):
    user_id = 0
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None
    if request.method == 'POST':
        user_id = user_data_handler.get_userid_by_username(user_name)
        user_id = user_id['id']
        add_dict = {'question_id': id_, 'user_id': user_id, 'comment': request.form['comment']}
        sql_handler.add_question_comment(add_dict)
    if comment_id is not None:
        where_url = url_for('edit_question_comment', comment_id=comment_id, id_=id_)
    else:
        where_url = url_for('show_question_comments', id_=id_)
    comments = sql_handler.get_question_comments(id_)
    question = sql_handler.get_question_details_by_id(id_)
    return render_template('comments.html',
                           comments=comments,
                           where_url=where_url,
                           question=question['message'],
                           question_title=question['title'],
                           back_url=url_for("show_question_details", id_=id_),
                           id_=id_,
                           comment_id=comment_id,
                           comment_to_edit=comment_message,
                           logged_in_as=session_name,
                           user_name=user_name, user_role=user_role, user_id=user_id)


@app.route("/edit-question", methods=['GET', 'POST'])
def edit_question_comment():
    if request.method == 'POST':
        sql_handler.edit_question_comment(
            {'comment_id': request.args['comment_id'], 'comment': request.form['comment']})
        return redirect(f"/show-comments/{request.args['id_']}")
    comment_details = sql_handler.get_comment(request.args['comment_id'])
    return redirect(
        f"/show-comments/{comment_details['question_id']}/{comment_details['id']}/{comment_details['comment']}")


@app.route("/edit-answer-comment", methods=['GET', 'POST'])
def edit_answer_comment():
    if request.method == "POST":
        sql_handler.edit_answer_comment({'comment_id': request.args['comment_id'], 'comment': request.form['comment']})
        return redirect(f"show-answer-comments/{request.args['question_id']}/{request.args['answer_id']}")
    comment_details = sql_handler.get_answer_comment(request.args['comment_id'])
    return redirect(
        f"show-answer-comments/{request.args['question_id']}/{comment_details['answer_id']}/{comment_details['id']}/{comment_details['comment']}"
    )


@app.route("/delete-comment/<comment_id>/<question_id>", methods=['GET', 'POST'])
def delete_question_comment(comment_id, question_id):
    sql_handler.delete_question_comment(comment_id)
    return redirect(f'/show-comments/{question_id}')


@app.route('/latest-question/', methods=["POST", "GET"])
def display_latest_question_by_id():
    user_id = 0
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None
    latest_question = sql_handler.display_latest_question()
    try:
        question_id = latest_question['id']
        question_user_id = latest_question['user_id']
    except KeyError:
        question_id = None
        question_user_id = None
    return render_template('latest_question.html',
                           latest_question=latest_question,
                           question_id=question_id,
                           logged_in_as=session_name,
                           user_name=user_name,
                           user_role=user_role,
                           user_id=user_id,
                           question_user_id=question_user_id
                           )


@app.route("/search/<search_phrase>/<dir_>", methods=["GET", "POST"])
def search(search_phrase, dir_):
    if 'username' in session:
        session_name = f"You are logged in as {escape(session['username'])}"
        user_name = escape(session['username'])
        user_id = int(escape(session['user_id']))
        user_role = user_data_handler.get_user_role(user_id)['role']
    else:
        session_name = 'You are not logged in'
        user_name = None
        user_role = None
    found_search = sql_handler.search_sort(dir_, search_phrase)
    return render_template("search.html",
                           search_phrase=search_phrase,
                           found_search=found_search,
                           dir_=dir_,
                           logged_in_as=session_name,
                           user_name=user_name,
                           user_role=user_role)


@app.route('/accept/<answer_id>/<id_>', methods=['GET', 'POST'])
def accept_answer(answer_id, id_):
    user_data_handler.mark_answer_as_accepted(answer_id, id_)
    return redirect(f"/question_details/{id_}")


if __name__ == "__main__":
    app.run(debug=True)
