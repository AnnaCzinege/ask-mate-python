from flask import Flask, request, render_template, redirect, url_for
import data_handler


app = Flask(__name__)
QUESTION_TABLE = 'sample_data/question.csv'


@app.route("/")
@app.route("/list")
def route_list():
    question_table = data_handler.get_data(QUESTION_TABLE)
    return render_template("list.html", question_table=question_table)


@app.route("/add_edit", methods=["POST", "GET"])
@app.route("/add_edit/<string:id_>", methods=["POST", "GET"])
def route_add_edit(id_=None):

    # When you click on an ID
    if request.method == "GET" and id_ is not None:
        table = data_handler.get_data(QUESTION_TABLE)
        row = data_handler.get_row_by_id(table, id_)
        row_id = row[0]
        row_title = row[1]
        row_message = row[2]
        return render_template("add_edit.html", id_=row_id, row_title=row_title, row_message=row_message, title="Edit question")

    # When you finished adding a new question
    if request.method == "POST" and id_ is None:
        row = [
            data_handler.generate_id(data_handler.get_data(QUESTION_TABLE)),
            request.form["title"],
            request.form["message"]
        ]
        data_handler.add_element(QUESTION_TABLE, row)
        return redirect("/")

    # When someone clicks on add new question button
    return render_template("add_edit.html", id_=None, title='Add new question')


@app.route("/question_details/<string:id_>")
def show_question_details(id_=None):
    table = data_handler.get_data(QUESTION_TABLE)
    row = data_handler.get_row_by_id(table, id_)
    row_title = row[1]
    row_question = row[2]
    return render_template("question_details.html", row_title=row_title, row_question=row_question)


if __name__ == "__main__":
    app.run(debug=True)