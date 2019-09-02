from flask import Flask, request, render_template, redirect, url_for
import data_handler
import sql_handler

app = Flask(__name__)


@app.route("/")
@app.route("/<int:num>")
@app.route("/show/<int:id_>", methods=["GET", "POST"])
@app.route("/list/<string:id_>", methods=["GET", "POST"])
def route_list(id_=None, num=None):
    id_title = sql_handler.get_question_id_title()
    '''question_table = data_handler.get_data()

    if num is not None:
        dir_ = request.args.get("dir_")
        question_table = data_handler.sort_columns(question_table, num, dir_)
        return render_template("list.html", question_table=question_table, dir_=dir_)

    '''

    return render_template("list.html", id_title=id_title)


@app.route("/delete/<int:id_>", methods=["POST", "GET"])
def route_delete(id_=None):
    if request.method == "POST":
        sql_handler.delete_question_by_id(id_)
        return redirect("/")

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
    '''
    # When you finished updating the question
    if request.method == "POST" and id_ is not None:
        row = [
            request.form["id_"],
            request.form["title"],
            request.form["message"]
        ]
        new_question_table = data_handler.edit_element(row, data_handler.get_data())
        data_handler.save_data(new_question_table)
        return redirect("/")

    # When you click on an ID
    if id_ is not None:
        table = data_handler.get_data()
        row = data_handler.get_row_by_id(table, id_)
        row_id = row[0]
        row_title = row[1]
        row_message = row[2]
        return render_template("add_edit.html", id_=row_id, row_title=row_title, row_message=row_message,
                               title="Edit question")
    '''


@app.route("/question_details/<string:id_>", methods=["GET", "POST"])
def show_question_details(id_=None):
    question = sql_handler.get_question_details_by_id(id_)
    answers = sql_handler.list_answers_by_question_id(id_)
    '''
    if request.method == "POST":  # When you submit an answer
        answer = request.form['answer']
        data_handler.add_answers(row_id, answer, answer_table)
        return redirect(url_for('show_question_details', id_=row_id))
    '''
    return render_template("question_details.html",
                           row_title=question['title'],
                           row_question=question['message'],
                           answer_list=answers,
                           where_url=url_for("show_question_details",
                                             id_=id_)
                           )

if __name__ == "__main__":
    app.run(debug=True)
