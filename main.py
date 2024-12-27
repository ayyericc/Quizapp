import random
import html
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify, session
from sqlalchemy.exc import IntegrityError
from unicodedata import category
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import secrets
import time

from db.main import db, Category, Questions, QuestionsMulti,Users, PastQuiz
from quiz import Quiz
import os

#creates an object with the quiz class
game = Quiz()


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(24)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'db', 'instance', 'questions.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


with app.app_context():
    db.create_all()





@app.route("/", methods= ["GET", "POST"])
def home():
    # Gets all the category's to send to the front end

    #Uses matching ids to get the category for that specific quiz. Also us dynamic for when I update categorys
    tf_matching_ids = db.session.query(Category.id, Category.category).join(Questions, Category.id == Questions.category_id).distinct().all()
    multi_matching_ids = db.session.query(Category.id, Category.category).join(QuestionsMulti, Category.id == QuestionsMulti.category_id).distinct().all()

    #Parses the tuples and get just the category to send to the front end
    true_false_categories = [html.unescape(cat[1]) for cat in tf_matching_ids]
    multi_choice_categories = [html.unescape(cat[1]) for cat in multi_matching_ids]


    if request.method == "POST":
        session["category"] = request.form.get("category")
        session.permanent = True

        quiz = request.form.get("quiz")
        if quiz == "multi":
            return redirect(url_for("multiple_choice"))

        elif quiz == "true_false":
            return redirect(url_for("true_false"))

    return render_template("index.html", multi_choice_categories= multi_choice_categories, true_false_categories= true_false_categories)




@app.route("/true_false", methods= ["GET","POST"])
def true_false():


    if request.method == "POST":

        #Get the user answers and return a score which is then passed to the html
        user_answer = [request.form.get(f"answer_{i}") for i in range(1, 11)]
        score = game.check_answer(user_input= user_answer, correct_answer= session["questions"])
        score_percentage = score * 10

        return render_template("results.html", score= score, score_percentage= score_percentage)
        # return jsonify(quiz= "if the user wants to take the quiz again")



    with app.app_context():
        #grabs the id of the chosen category
        chosen_category = session["category"]
        category_id = db.session.query(Category).filter(Category.category == chosen_category).first()


        #parses the db and return the correct questions
        temp_questions = db.session.query(Questions).filter(Questions.category_id == category_id.id)
        questions_list = [[temp.question, temp.answer] for temp in temp_questions]

    #Uses a method in the Quiz class to return 10 questions to show the user
    questions = game.pick_10(questions_list) #questions along with the answer are now saved and ready for the front end
    session["questions"] = questions

    return render_template("true_false.html", questions= questions)







@app.route("/multiple_choice", methods= ["GET", "POST"])
def multiple_choice():

    if request.method == "POST":
        user_answer = [request.form.get(f"answer_{i}") for i in range(1, 11)]
        questions = session["questions"]

        score = game.check_answer(user_input=user_answer, correct_answer=session["questions"]) * 10

        return render_template("results.html", score= score)

    with app.app_context():
        # grabs the id of the chosen category
        chosen_category = session["category"]
        category_id = db.session.query(Category).filter(Category.category == chosen_category).first()

        # parses the db and return the correct questions
        temp_questions = db.session.query(QuestionsMulti).filter(QuestionsMulti.category_id == category_id.id).all()
        questions_list = [[temp.question, temp.answer, temp.option1, temp.option2, temp.option3, temp.option4] for temp in temp_questions]

        # Uses a method in the Quiz class to return 10 questions to show the user
        questions = game.pick_10(questions_list)  # questions along with the answer are now saved and ready for the front end
        choices = [[choice[2], choice[3], choice[4], choice[5]] for choice in questions]
        for choice in choices: #Shuffles the list of choices before sending to the front-end
            random.shuffle(choice)


        session["questions"] = questions
        questions_with_choices = zip(questions, choices) #Only using the zip function cause ChatGBT didn't write the front end correctly

    return render_template("multi_choice.html", questions_with_choices= questions_with_choices)





@app.route("/register", methods= ["POsT", "GET"])
def register():

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        result = db.session.query(Users).filter(Users.email == email).first()

        if not result:
            user = Users(email= email,
                         name= name,
                         password= generate_password_hash(password, salt_length= 8, method= "pbkdf2:sha256"))
            db.session.add(user)
            db.session.commit()
            return jsonify(user= "user successfully created")

        else:
            return jsonify(user= "user already exist")



    return jsonify(test= "home page")





@app.route("/login", methods= ["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        result = db.session.query(Users).filter_by(Users.email == email).first()

        if result and check_password_hash(password, result.password):
            return jsonify(result= "successfully logged")

        else:
            flash("email dont exist. Register a new account")
            return redirect(url_for("register"))

    return jsonify(test= "Homepage")









if __name__ == "__main__":
    app.run(debug= True)




























