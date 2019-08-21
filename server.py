from flask import Flask, request, render_template, redirect, url_for
import data_handler


app = Flask(__name__)
QUESTION_TABLE = "question.csv"


@app.route("/")
def route_list():
    question_table = data_handler.get_data(QUESTION_TABLE)
    return render_template("list.html", question_table=question_table)


@app.route("/add_edit", methods=["POST", "GET"])
@app.route("/add_edit/<int:id>", methods=["POST", "GET"])
def route_add_edit(id=None):

    if request.method == "GET" and id is not None:  # When someone clicks on a title
        row = get_row_by_id(get_table(TABLE), id)
        return render_template("add_edit.html", row=row)

    return render_template("add_edit.html", id=None)  # When someone clicks on add new question button


if __name__ == "__main__":
    app.run(debug=True)