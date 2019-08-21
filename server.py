from flask import Flask, request, render_template, redirect, url_for
import data_handler


app = Flask(__name__)
QUESTION_TABLE = 'sample_data/question.csv'


def generate_id():
    return len(data_handler.get_data(QUESTION_TABLE))+1


@app.route("/")
@app.route("/list")
def route_list():
    question_table = data_handler.get_data(QUESTION_TABLE)
    return render_template("list.html", question_table=question_table)


@app.route("/add_edit", methods=["POST", "GET"])
@app.route("/add_edit/<int:id>", methods=["POST", "GET"])
def route_add_edit(id_=None):

    if request.method == "GET" and id_ is not None:  # When you click on a title
        table = data_handler.get_data(QUESTION_TABLE)
        row = data_handler.get_row_by_id(table, id_)
        row_id = row[0]
        row_title = row[1]
        row_message = row[2]
        return render_template("add_edit.html", id_=row_id, row_title=row_title, row_message=row_message, title="Edit question")

    if request.method == "POST" and id_ is None: # When you finished adding a new question
        row = [
            generate_id(),
            request.form["title"],
            request.form["message"]
        ]
        data_handler.append_table(QUESTION_TABLE, row)
        return redirect("/")

    return render_template("add_edit.html", id_=None, title='Add new question')  # When someone clicks on add new question button


@app.route("/question_details/<int:id>")
def show_question_details(id=None):
    table = data_handler.get_data(QUESTION_TABLE)
    row = data_handler.get_row_by_id(table, id)
    row_title = row[1]
    row_question = row[2]
    return render_template("question_details.html", row_title=row_title, row_question=row_question)


if __name__ == "__main__":
    app.run(debug=True)