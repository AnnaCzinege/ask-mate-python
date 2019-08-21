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
@app.route("/add_edit/<int:id>", methods=["POST", "GET"])
def route_add_edit(id=None):

    if request.method == "GET" and id is not None:  # When someone clicks on a title
        table = data_handler.get_data(QUESTION_TABLE)
        row = data_handler.get_row_by_id(table, id)
        row_id = row[0]
        row_title = row[1]
        row_message = row[2]
        return render_template("add_edit.html", row_id=row_id, row_title=row_title, row_message=row_message)

    return render_template("add_edit.html", id=None)  # When someone clicks on add new question button


@app.route("/question_details")
def show_question_details():


if __name__ == "__main__":
    app.run(debug=True)