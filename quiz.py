import html
import requests

api_url = "https://opentdb.com/api.php?amount=10&type=boolean"


class Quiz:
    def __init__(self):
        self.score = 0
        self.question_count = 1
        self.question_list = {}


    def question_dict(self):
        response = requests.get(api_url)

        data = response.json()
        questions = data["results"]

        for i, question in enumerate(questions):
            self.question_list[i] = {
                "question": html.unescape(questions[self.question_count]["question"]),
                "answer": html.unescape(questions[self.question_count]["correct_answer"]),

            }

        return self.question_list

    def check_answer(self, user_input, correct_answer):
        if user_input.lower() == correct_answer.lower():
            self.score += 1
            return True

        self.question_count += 1
        return False

    def finished(self):
        return f"Your final score was {self.score}/{self.question_count}"












































