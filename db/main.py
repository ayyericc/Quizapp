from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Integer, String, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
import requests
import html
import time


db = SQLAlchemy()

#INIT the Alchemy library and also I created the tables ima use to store the category and questions
class Base(DeclarativeBase):
    pass


class Category(db.Model):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    category: Mapped[str] = mapped_column(String, unique= True, nullable= False)

    #creates the relationship between the Questions table
    question = relationship("Questions", back_populates= "category", cascade= "all, delete-orphan")
    questions_multi = relationship("QuestionsMulti", back_populates= "category", cascade= "all, delete-orphan")

class Questions(db.Model):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable= False)
    question: Mapped[str] = mapped_column(String(150), unique= True, nullable= False)
    answer: Mapped[str] = mapped_column(String(10), nullable= False)

    #creates relationship with Category table
    category = relationship("Category", back_populates= "question")

class QuestionsMulti(db.Model):
    __tablename__ = "questions_multi"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable= False)
    question: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    answer: Mapped[str] = mapped_column(String(50), nullable=False)
    option1: Mapped[str] = mapped_column(String(50), nullable= False)
    option2: Mapped[str] = mapped_column(String(50), nullable= False)
    option3: Mapped[str] = mapped_column(String(50), nullable= False)
    option4: Mapped[str] = mapped_column(String(50), nullable= False)


    category = relationship("Category", back_populates= "questions_multi")

class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    name: Mapped[str] = mapped_column(String(50), nullable= False)
    email: Mapped[str] = mapped_column(String(100), nullable= False, unique= True)
    password: Mapped[int] = mapped_column(Integer, nullable= False)

    pastquiz = relationship("PastQuiz", back_populates= "users", cascade= "all, delete-orphan")

class PastQuiz(db.Model):
    __tablename__ = "pastquiz"

    id: Mapped[int] = mapped_column(Integer, primary_key= True, unique= True)
    users_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable= False)
    question: Mapped[str] = mapped_column(String, nullable= False)
    answer: Mapped[str] = mapped_column(String, nullable= False)
    date: Mapped[int] = mapped_column(Integer, nullable= False)


    users = relationship("Users", back_populates= "pastquiz")





# # Set up the database
# DATABASE_URL = "sqlite:///instance/questions.db"
# engine = create_engine(DATABASE_URL)
#
# # Create tables
# Base.metadata.create_all(engine)
#
# # Create a session for database operations
# Session = sessionmaker(bind=engine)
# session = Session()



# #Loops through all the categorys and add questions to the DB``
# is_running = 0
# while is_running != 32:
#
#     url = f"https://opentdb.com/api.php?amount=40&category={is_running}&type=multiple"
#     response = requests.get(url)
#     data = response.json()
#     unfilterd_data = data["results"]
#
#
#     if unfilterd_data:
#         category_placeholder = html.unescape(data["results"][0]["category"])
#         questions_list = []
#
#         for question in unfilterd_data:
#
#             questions_list.append([html.unescape(question["question"]),
#                                    html.unescape(question["correct_answer"]),
#                                    html.unescape(question["incorrect_answers"][0]),
#                                    html.unescape(question["incorrect_answers"][1]),
#                                    html.unescape(question["incorrect_answers"][2]),
#                                    ])
#
#         print(category_placeholder)
#
#         # #adds the category to the Category table
#         try:
#             category = Category(category=category_placeholder)
#             session.add(category)
#             session.commit()
#         except IntegrityError as e:
#             session.rollback()
#         else:
#             pass
#
#         # grabs the primary key of the category I want to add the questions too
#         temp_category_id = session.query(Category).filter(Category.category == category_placeholder).first()
#
#         for question in questions_list:
#             # already_added = session.query(Questions).filter(Questions.question == question).first()
#             # if not already_added:
#             try:
#                 temp = QuestionsMulti(category_id=temp_category_id.id,
#                                       question=question[0],
#                                       answer=question[1],
#                                       option1= question[1],
#                                       option2= question[2],
#                                       option3= question[3],
#                                       option4= question[4])
#                 session.add(temp)
#                 session.commit()
#
#             except IntegrityError as e:
#                 session.rollback()
#
#             else:
#                 continue
#         print("already in db")
#
#     else:
#         print(f"Category {is_running} was skipped")
#
#     is_running += 1
#     time.sleep(15)
#
# print("all questions added to the db")



#------------------------------------------------Grab True/False questions------------------------------------------------------------------------------
# for question in unfilterd_data:
#     questions_list.append([html.unescape(question["question"]), html.unescape(question["correct_answer"])])
#
# # print(questions_list)
# print(category_placeholder)
#-------------------------------------------------------------------------------------------------------------------------------------













