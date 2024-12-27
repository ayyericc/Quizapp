import html
import requests
import random



api_url = "https://opentdb.com/api.php?amount=10&type=boolean"


class Quiz:
    def __init__(self):
        self.score = 0
        self.question_count = 1
        self.question_list = {}

    #This method is not being used since I made my own DB -------------------------------
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

    def check_answer(self, user_input, correct_answer, multi= False):
        correct_answers = [answer[1] for answer in correct_answer]

        for i, answer in enumerate(user_input):
            if correct_answers[i] == answer:
                self.score += 1
            else:
                continue

        return self.score


    def finished(self):
        return f"Your final score was {self.score}/{self.question_count}"

    def pick_10(self, question_list):
        temp_list = []
        count = 0

        while count < 10:
            temp_question = random.choice(question_list)

            if temp_question not in temp_list:
                temp_list.append(html.unescape(temp_question))
                count += 1
            else:
                continue


        return temp_list








7




































