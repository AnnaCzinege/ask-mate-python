from flask import Flask, request, render_template, redirect, url_for
import sql_handler

app = Flask(__name__)


@app.route("/")
@app.route("/<int:num>")
@app.route("/show/<int:id_>", methods=["GET", "POST"])
@app.route("/list/<string:id_>", methods=["GET", "POST"])
def route_list(id_=None, num=None):
    id_title = sql_handler.get_question_id_title()
    if num is not None:
        dir_ = request.args.get("dir_")
        id_title = sql_handler.sort_questions(dir_)
        return render_template("list.html", id_title=id_title, dir_=dir_)
    return render_template("list.html", id_title=id_title)


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
    # When finished adding
    if request.method == "POST":
        row = {'title': str(request.form["title"]), 'message': str(request.form["message"])}
        sql_handler.add_new_question(row)
        return redirect("/")

    # When someone clicks on add new question button
    return render_template("add_edit.html", id_=None, title='Add new question')


@app.route("/edit", methods=["POST", "GET"])
@app.route("/edit/<id_>", methods=["POST", "GET"])
def route_edit(id_=None):
    # When you finished updating the question
    if request.method == "POST" and id_ is not None:
        updated_row = {'id': request.form["id_"], 'title': request.form["title"], 'message': request.form["message"]}
        sql_handler.edit_question(updated_row)
        return redirect("/")

    # When you click the edit action button
    if id_ is not None:
        question = sql_handler.get_question_details_by_id(id_)
        return render_template("add_edit.html", id_=question['id'], row_title=question['title'], row_message=question['message'],
                               title="Edit question")


@app.route("/question_details/<id_>", methods=['GET', 'POST'])
@app.route("/question_details/<id_>/<answer_message>", methods=["GET", "POST"])
def show_question_details(id_=None, answer_message=''):
    question = sql_handler.get_question_details_by_id(id_)
    answers = sql_handler.list_answers_by_question_id(id_)
    comment_number = sql_handler.count_comments_for_question(id_)
    list_of_comment_numbers_on_answers = []

    for item in answers:
        answer_id = item['id']
        num_of_comments = sql_handler.count_comments_for_answer(answer_id)
        list_of_comment_numbers_on_answers.append(num_of_comments)

    if request.method == "POST":  # When you submit an answer
        answer = {'id': id_, 'message': str(request.form['answer'])}
        sql_handler.add_new_answer(answer)
        return redirect(url_for('show_question_details', id_=id_))
    
    return render_template("question_details.html",
                           row_title=question['title'],
                           row_question=question['message'],
                           answer_list=answers,
                           where_url=url_for("show_question_details", id_=id_),
                           comment_number=comment_number,
                           comment_number_answer=list_of_comment_numbers_on_answers,
                           id_=id_,
                           answer_message=answer_message
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
    return redirect(f'/question_details/{question_id}/{answer_message}')


@app.route("/delete-answer/<answer_id>", methods=["POST", "GET"])
def delete_answer(answer_id):
    answer = sql_handler.get_answer_by_answer_id(answer_id)
    question_id = answer['question_id']
    if request.method == "POST":
        sql_handler.delete_answer(answer_id)
        return redirect(f"/question_details/{question_id}")


@app.route("/show-comments/<id_>", methods=['GET', 'POST'])
def show_question_comments(id_):
    if request.method == 'POST':
        add_dict = {'question_id': id_, 'comment': request.form['comment']}
        sql_handler.add_question_comment(add_dict)
    comments = sql_handler.get_question_comments(id_)
    question = sql_handler.get_question_details_by_id(id_)
    return render_template('comments.html',
                           comments=comments,
                           where_url=url_for('show_question_comments', id_=id_),
                           question=question['message'],
                           question_title=question['title'],
                           back_url=url_for("show_question_details", id_=id_)
                           )


@app.route('/latest-question/', methods=["POST", "GET"])
def display_latest_question_by_id():
    latest_question = sql_handler.display_latest_question()
    question_id = latest_question['id']
    return render_template('latest_question.html', latest_question=latest_question, question_id=question_id)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        found_search = sql_handler.search_by_phrase(request.form['search_phrase'])
        return render_template("/search.html", found_search=found_search)
    elif request.method == "GET":
        return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
