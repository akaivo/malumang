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
    ops.map(lambda questions: random.sample(questions, len(questions)))
)

next_question_subject = Subject()
question_observable = games_observable.pipe(
    ops.map(lambda questions: rx.zip(rx.from_iterable(questions), rx.merge(next_question_subject, app.start_subject))),
    ops.switch_latest(),
    ops.map(lambda t: t[0]),
    ops.map(lambda q: { **q, 'timestamp': datetime.datetime.now()})
)

def check_question(pair):
    print(pair)
    next_question_subject.on_next(None)

question_observable.subscribe(
  on_next=app.display_question,
  scheduler=scheduler  
)

def is_new_answer(qa):
    question = qa[0]
    answer = qa[1]
    return answer['timestamp'] > question['timestamp']

app.answer_subject.subscribe(on_next=print, scheduler=scheduler)
question_observable.subscribe(on_next=print, scheduler=scheduler)

rx.combine_latest(question_observable, app.answer_subject).pipe(
    ops.filter(is_new_answer)
).subscribe(
    on_next=wrap("check", check_question),
    on_completed=lambda: app.show_frame(ScoreScreen),
    scheduler=scheduler  
)
app.mainloop()
