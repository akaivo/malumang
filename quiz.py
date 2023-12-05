import datetime
import json
import random
import tkinter as tk

import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler.mainloop import TkinterScheduler
from reactivex.subject import Subject

from ui import QuestionScreen, QuizApp, ScoreScreen, StartScreen


def debug(id):
    def show(text):
        print(f"{id} : {text}")
    return show
def wrap(id, f):
    def wrap_function(value):
        print("wrap " + id)
        f(value)
    return wrap_function

def load_questions(filename):
    with open(filename, 'r') as file:
        return json.load(file)

app = QuizApp()
scheduler = TkinterScheduler(app)

games_observable = app.restart_subject.pipe(
    ops.start_with(None),
    ops.do_action(on_next=lambda _questions: app.show_frame(StartScreen)),
    ops.map(lambda _: load_questions("questions.json")),
    ops.map(lambda questions: random.sample(questions, len(questions))),
    ops.map(lambda questions: [
        {**question, 'is_last': index == len(questions) - 1} for index, question in enumerate(questions)
    ])
)

next_question_subject = Subject()
question_observable = games_observable.pipe(
    ops.map(lambda questions: rx.zip(rx.from_iterable(questions), rx.merge(next_question_subject, app.start_subject))),
    ops.switch_latest(),
    ops.map(lambda t: t[0]),
    ops.map(lambda q: { **q, 'timestamp': datetime.datetime.now()})
)

question_observable.subscribe(
  on_next=print,
  scheduler=scheduler  
)
question_observable.subscribe(
  on_next=app.display_question,
  scheduler=scheduler  
)

def is_new_answer(qa):
    question = qa[0]
    answer = qa[1]
    return answer['timestamp'] > question['timestamp']

answer_observable = rx.combine_latest(question_observable, app.answer_subject).pipe(
    ops.filter(is_new_answer),
    ops.do_action(print)
)

answer_observable.pipe(
    ops.delay(1)
).subscribe(
    on_next=(lambda _: next_question_subject.on_next(None)),
    scheduler=scheduler  
)

def check_answer(qa_pair):
    q, a = qa_pair
    return q["correct"] == a["answer"]

correct_answers, wrong_answers = answer_observable.pipe(ops.partition(check_answer))

correct_answers.subscribe(
    on_next=lambda qa: print(f"Correct: {qa[0]['question']} - {qa[0]['answers'][qa[1]['answer']]}"),
    scheduler=scheduler
)
wrong_answers.subscribe(
    on_next=lambda qa: print(f"Wrong: {qa[0]['question']} - {qa[0]['answers'][qa[1]['answer']]}"),
    scheduler=scheduler
)
app.mainloop()
