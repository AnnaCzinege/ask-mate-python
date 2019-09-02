from flask import Flask, request, render_template, redirect, url_for
import data_handler


app = Flask(__name__)


@app.route("/")
@app.route("/<int:num>")
@app.route("/show/<int:id_>", methods=["GET", "POST"])
@app.route("/list/<string:id_>", methods=["GET", "POST"])
def route_list(id_=None, num=None):
    question_table = data_handler.get_data()
    if num is not None:
        dir_ = request.args.get("dir_")
        question_table = data_handler.sort_columns(question_table, num, dir_)
        return render_template("list.html", question_table=question_table, dir_=dir_)
    if request.method == "POST":
        question_table = data_handler.remove_element(question_table, id_)
        data_handler.save_data(question_table)
        return redirect("/")
    return render_template("list.html", question_table=question_table)


@app.route("/add", methods=["POST", "GET"])
def route_add():

    # When you finished adding a new question
    if request.method == "POST":
        row = [
            data_handler.generate_id(data_handler.get_data()),
            request.form["title"],
            request.form["message"]
        ]
        data_handler.add_element(row)
        return redirect("/")

    # When someone clicks on add new question button
    return render_template("add_edit.html", id_=None, title='Add new question')


@app.route("/edit", methods=["POST", "GET"])
@app.route("/edit/<id_>", methods=["POST", "GET"])
def route_edit(id_=None):

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


@app.route("/question_details/<string:id_>", methods=["GET", "POST"])
def show_question_details(id_=None):
    table = data_handler.get_data()
    answer_table = data_handler.get_answers()
    answer_list = data_handler.get_list_from_dict(answer_table, id_)
    row = data_handler.get_row_by_id(table, id_)
    row_id = row[0]
    row_title = row[1]
    row_question = row[2]
    if request.method == "POST":
        answer = request.form['answer']
        data_handler.add_answers(row_id, answer, answer_table)
        return redirect(url_for('show_question_details', id_=row_id))
    return render_template("question_details.html",
                           row_title=row_title,
                           row_question=row_question,
                           answer_list=answer_list,
                           where_url=url_for("show_question_details", id_=row_id)
                           )


if __name__ == "__main__":
    app.run(debug=True)