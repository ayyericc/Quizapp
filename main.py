from flask import Flask, request, jsonify
from quiz import Quiz

game = Quiz()

app = Flask(__name__)



@app.route("/", methods= ["GET", "POST"])
def home():

    if request.method == "POST":
        question_dict = game.question_dict()
        for question, answer in question_dict.items():
            temp_ques = question
            print(question)
            temp_answer = answer
            user_input = request.form.get("user_input")
            game.check_answer(user_input, answer)





    return jsonify(home= "homepage")











if __name__ == "__main__":
    app.run(debug= True)




























