from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify, session
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import secrets
import time

from db.main import db, Category, Questions, QuestionsMulti
from quiz import Quiz
import os


game = Quiz()

app = Flask(__name__)

base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'db', 'instance', 'questions.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/", methods= ["GET", "POST"])
def home():

    if request.method == "POST":
        quiz = request.form.get("quiz")
        if quiz == "true_false":
            session["category"] = request.form.get("category")
            return redirect(url_for("multiple_choice"))

        elif quiz == "multi":
            session["category"] = request.form.get("category")
            return redirect(url_for("true_false"))



    return jsonify(home= "homepage")

@app.route("/true_false", methods= ["GET","POST"])
def true_false():


    if request.method == "POST":
        return jsonify(quiz= "if the user wants to take the quiz again")



    with app.app_context():
        #grabs the id of the chosen category
        # chosen_category = session["category"]
        chosen_category = request.form.get("cat")
        category_id = db.session.query(Category).filter(Category.category == chosen_category).first()


        #parses the db and return the correct questions
        temp_questions = db.session.query(Questions).filter(Questions.category_id == category_id.id)
        questions_list = [[temp.question, temp.answer] for temp in temp_questions]

    #Uses a method in the Quiz class to return 10 questions to show the user
    questions = game.pick_10(questions_list) #questions along with the answer are now saved and ready for the front end


    return jsonify(test= questions)

@app.route("/multiple_choice", methods= ["GET", "POST"])
def multi_choice():

    if request.method == "POST":
        return jsonify(test= "Test post method")

    with app.app_context():
        # grabs the id of the chosen category
        # chosen_category = session["category"]
        chosen_category = request.form.get("cat")
        category_id = db.session.query(Category).filter(Category.category == chosen_category).first()

        # parses the db and return the correct questions
        temp_questions = db.session.query(QuestionsMulti).filter(Questions.category_id == category_id.id)
        questions_list = [[temp.question, temp.answer, temp.option1, temp.option2, temp.option3, temp.option4] for temp in temp_questions]

        # Uses a method in the Quiz class to return 10 questions to show the user
        questions = game.pick_10(questions_list)  # questions along with the answer are now saved and ready for the front end

    return jsonify(test= questions)











if __name__ == "__main__":
    app.run(debug= True)




























