import json
import os
import random


class Game:
  def __init__(self, current_language):
    file_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(file_dir, f"questions_{current_language}.json")
    self.__questions = self.load_questions(abs_file_path)
    random.shuffle(self.__questions)
    self.__current_question_index = 0
    self.__total = len(self.__questions)
    self.__correct_answers = 0

  def current_question(self):
     return self.__questions[self.__current_question_index]
  
  def load_questions(self, filename):
    with open(filename, 'r') as file:
        return json.load(file)
  
  def check_answer(self, answer):
     correct_answer = self.current_question()["correct"]
     if(correct_answer == answer):
        self.__correct_answers += 1
     return correct_answer

  def next_question(self):
     self.__current_question_index += 1
     return self.__current_question_index < self.__total
  
  def result(self):
     return self.__correct_answers, self.__total