import json
import random
import tkinter as tk

import reactivex as rx
from reactivex import operators as ops
from reactivex.scheduler.mainloop import TkinterScheduler
from reactivex.subject import Subject

from ui import QuestionScreen, QuizApp, ScoreScreen, StartScreen


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

question_observable = games_observable.pipe(
    ops.map(lambda questions: rx.from_iterable(questions)),
    ops.switch_latest()
)

question_observable.subscribe(on_next=print)

next_question_observable = Subject()
def check_question(pair):
    # print(pair)
    next_question_observable.on_next(None)

rx.zip(question_observable, rx.merge(next_question_observable, app.start_subject)).pipe(
   ops.map(lambda t: t[0])
  ).subscribe(
  on_next=app.display_question,
  scheduler=scheduler  
)

rx.zip(question_observable, app.answer_subject).subscribe(
    on_next=check_question,
    on_completed=lambda: app.show_frame(ScoreScreen),
    scheduler=scheduler  
)
app.mainloop()
