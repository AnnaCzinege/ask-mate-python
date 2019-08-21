from flask import Flask, request, render_template, redirect, url_for
import data_handler


app = Flask(__name__)
QUESTION_TABLE = "question.csv"


@app.route("/")
def route_list():
    question_table = data_handler.get_data(QUESTION_TABLE)
    return render_template("list.html", question_table=question_table)


if __name__ == "__main__":
    app.run(debug=True)