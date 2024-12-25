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

game = Quiz()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/instance/questions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)



@app.route("/", methods= ["GET", "POST"])
def home():

    # if request.method == "POST":
    #     question_dict = game.question_dict()
    #     for key, answer in question_dict.items():
    #         temp_ques = answer["question"]
    #         temp_answer = answer["answer"]
    #         user_input = request.form.get("user_input")
    #         return jsonify(answer= game.check_answer(user_input= user_input, correct_answer= temp_answer))

    with app.app_context():
        try:
            with app.app_context():
                result = db.session.execute(db.select(Category))
                return jsonify(data= result)

        except IntegrityError as e:
            print("failed to open file")
        else:

            return jsonify(error= "failed")





    return jsonify(home= "homepage")











if __name__ == "__main__":
    app.run(debug= True)




























