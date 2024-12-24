from flask import Flask, request, jsonify
from quiz import Quiz

game = Quiz()

app = Flask(__name__)



@app.route("/", methods= ["GET", "POST"])
def home():

    if request.method == "POST":
        question_dict = game.question_dict()
        for key, answer in question_dict.items():
            temp_ques = answer["question"]
            temp_answer = answer["answer"]
            user_input = request.form.get("user_input")
            return jsonify(answer= game.check_answer(user_input= user_input, correct_answer= temp_answer))






    return jsonify(home= "homepage")











if __name__ == "__main__":
    app.run(debug= True)




























