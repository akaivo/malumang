import tkinter as tk
from tkinter import font as tkFont

from game import Game

PADDING = 10
BG = "green"
QUESTION_DELAY = 1000
FONT = "Helvetica"
FONT_SIZE = 24

class StartScreen(tk.Frame):
    def __init__(self, parent, start_callback):
        tk.Frame.__init__(self, parent, bg=BG)
        start_button = tk.Button(
            self, text="Alusta mängu!",
            command=start_callback,
            relief=tk.FLAT,
            font=tkFont.Font(family=FONT, size=FONT_SIZE)
        )
        start_button.place(
            x=PADDING,
            y=PADDING,
            width=parent.winfo_width() - 2*PADDING,
            height=parent.winfo_height() - 2*PADDING
        )

class QuestionScreen(tk.Frame):
    def __init__(self, parent, answer_callback):
        tk.Frame.__init__(self, parent, bg=BG)
        self.question_label = tk.Label(self, text="Küsimus", bg='white')
        self.question_label.place(
           x=PADDING,
           y=PADDING,
           height=parent.winfo_height() * 0.75 - 2 * PADDING,
           width=parent.winfo_width() - 2 * PADDING
        )

        answers_frame = tk.Frame(self, bg=BG)
        answers_frame.place(
           x=PADDING,
           y=parent.winfo_height() * 0.75,
           height=parent.winfo_height() * 0.25 - PADDING,
           width=parent.winfo_width() - 2 * PADDING)

        w = parent.winfo_width() - 2 * PADDING
        h = parent.winfo_height() * 0.25 - PADDING
        x = 0.5 * w + 0.5 * PADDING
        y = 0.5 * h + 0.5 * PADDING

        self.answers = []
        answer_1 = tk.Label(answers_frame, text=f"Vastus 1", bg='white')
        answer_1.bind('<Button-1>', lambda _: answer_callback(0))
        answer_1.place(x=0, y=0, height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_1)

        answer_2 = tk.Label(answers_frame, text=f"Vastus 2", bg='white')
        answer_2.bind('<Button-1>', lambda _: answer_callback(1))
        answer_2.place(x=(0.5*w + 0.5*PADDING), y=0, height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_2)

        answer_3 = tk.Label(answers_frame, text=f"Vastus 3", bg='white')
        answer_3.bind('<Button-1>', lambda _: answer_callback(2))
        answer_3.place(x=0, y=(0.5*h + 0.5*PADDING), height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_3)

        answer_4 = tk.Label(answers_frame, text=f"Vastus 4", bg='white')
        answer_4.bind('<Button-1>', lambda _: answer_callback(3))
        answer_4.place(x=(0.5*w + 0.5*PADDING), y=(0.5*h + 0.5*PADDING), height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_4)

    def fill_question(self, question):
        self.question_label.configure(text=question["question"])
        for i in range(4):
          self.answers[i].configure(
              text=question["answers"][i],
              bg="white"
          )
        return self
    
    def highlight(self, given_answer, correct_answer):
        self.answers[correct_answer].configure(bg="light green")
        if(given_answer != correct_answer):
            self.answers[given_answer].configure(bg="red")
        return self
    
class ScoreScreen(tk.Frame):
    def __init__(self, parent, restart_callback):
        tk.Frame.__init__(self, parent, bg=BG)
        self.score_label = tk.Label(self, text="Sinu punktid: 10/10 !")
        self.score_label.place(
            x=PADDING,
            y=PADDING,
            width=parent.winfo_width() - 2*PADDING,
            height=parent.winfo_height() - 2*PADDING
        )
        self.score_label.bind("<Button-1>", lambda x: restart_callback())

    def update(self, score, total):
        self.score_label.configure(text=f"Sinu punktid: {score}/{total} !")

class QuizApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.game = Game()
        self.answer_locked = False

        self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda x: self.destroy())
        self.bind('1', lambda _: self.restart_game())

        self.update_idletasks()

        self.frames = {}
        frame = StartScreen(parent=self, start_callback=self.start_game)
        self.frames[StartScreen] = frame
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        frame = QuestionScreen(parent=self, answer_callback=self.check_answer)
        self.frames[QuestionScreen] = frame
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)
        
        
        frame = ScoreScreen(parent=self, restart_callback=self.restart_game)
        self.frames[ScoreScreen] = frame
        frame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.show_frame(StartScreen)

    def restart_game(self):
        self.game = Game()
        self.show_frame(StartScreen)

    def start_game(self):
        self.display_question(self.game.current_question())
    
    def next_question(self):
        self.answer_locked = False
        if(self.game.next_question()):
            self.display_question(self.game.current_question())
        else:
            self.show_score()

    def check_answer(self, answer):
        if(self.answer_locked):
            return 
        
        self.answer_locked = True
        correct = self.game.check_answer(answer)
        self.display_question(self.game.current_question()).highlight(answer, correct)
        self.after(QUESTION_DELAY, self.next_question)
    
    def display_question(self, question):
        return self.show_frame(QuestionScreen).fill_question(question)

    def show_score(self):
        score, total = self.game.result()
        self.show_frame(ScoreScreen).update(score, total)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        return frame
    
app = QuizApp()
app.mainloop()