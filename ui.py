import tkinter as tk
from tkinter import font as tkFont

from game import Game
from languages import languages
from physical_buttons import PhysicalButtons

PADDING = 10
BG = "green"
QUESTION_DELAY = 1000
FONT = "Helvetica"
FONT_SIZE = 32

class StartScreen(tk.Frame):
    def __init__(self, parent, start_callback, next_language_callback):
        tk.Frame.__init__(self, parent, bg=BG)
        self.start_button = tk.Label(
            self, text="Alusta mängu!",
            relief=tk.FLAT,
            bg="white",
            font=tkFont.Font(family=FONT, size=FONT_SIZE)
        )
        self.start_button.bind("<Button-1>", lambda _: start_callback())
        self.start_button.place(
            x=PADDING,
            y=PADDING,
            width=parent.winfo_width() - 2*PADDING,
            height=parent.winfo_height() - 2*PADDING
        )

        self.language_button = tk.Label(
            self, text="est",
            relief=tk.FLAT,
            bg="white",
            font=tkFont.Font(family=FONT, size=FONT_SIZE)
        )
        self.language_button.bind("<Button-1>", lambda _: next_language_callback())
        self.language_button.place(
            x=parent.winfo_width() * 1 - parent.winfo_height() * 0.125,
            y=parent.winfo_height() * (1 - 0.125),
            width=parent.winfo_height() * 0.124 - PADDING,
            height=parent.winfo_height() * 0.124 - PADDING
        )

    def set_language(self, new_language):
        self.start_button.configure(text=languages[new_language]['start_game'])
        self.language_button.configure(text=languages[new_language]['lang'])
    
class QuestionScreen(tk.Frame):
    def __init__(self, parent, answer_callback):
        tk.Frame.__init__(self, parent, bg=BG)
        self.question_label = tk.Label(
            self,
            text="Küsimus",
            bg='white',
            font=tkFont.Font(family=FONT, size=FONT_SIZE)
        )
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
        answer_1 = tk.Label(answers_frame, text=f"Vastus 1", bg='white', font=tkFont.Font(family=FONT, size=FONT_SIZE))
        answer_1.bind('<Button-1>', lambda _: answer_callback(0))
        answer_1.place(x=0, y=0, height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_1)

        answer_2 = tk.Label(answers_frame, text=f"Vastus 2", bg='white', font=tkFont.Font(family=FONT, size=FONT_SIZE))
        answer_2.bind('<Button-1>', lambda _: answer_callback(1))
        answer_2.place(x=(0.5*w + 0.5*PADDING), y=0, height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_2)

        answer_3 = tk.Label(answers_frame, text=f"Vastus 3", bg='white', font=tkFont.Font(family=FONT, size=FONT_SIZE))
        answer_3.bind('<Button-1>', lambda _: answer_callback(2))
        answer_3.place(x=0, y=(0.5*h + 0.5*PADDING), height=0.5*(h - PADDING), width=0.5*(w - PADDING))
        self.answers.append(answer_3)

        answer_4 = tk.Label(answers_frame, text=f"Vastus 4", bg='white', font=tkFont.Font(family=FONT, size=FONT_SIZE))
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
        self.score_label = tk.Label(
            self,
            text="Sinu punktid: 10/10 !",
            bg="white",
            font=tkFont.Font(family=FONT, size=FONT_SIZE)
        )
        self.score_label.place(
            x=PADDING,
            y=PADDING,
            width=parent.winfo_width() - 2*PADDING,
            height=parent.winfo_height() - 2*PADDING
        )
        self.score_label.bind("<Button-1>", lambda x: restart_callback())

    def update(self, score, total, current_language):
        self.score_label.configure(text=f"{languages[current_language]['your_score']} {score}/{total} !")

class QuizApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.current_language = 'estonian'
        self.game = Game(self.current_language)
        self.buttons = PhysicalButtons()
        self.answer_locked = False

        self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda x: self.destroy())
        self.bind('1', lambda _: self.restart_game())

        self.update_idletasks()

        self.frames = {}
        frame = StartScreen(parent=self, start_callback=self.start_game, next_language_callback=self.next_language)
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
        self.show_frame(StartScreen)

    def start_game(self):
        self.game = Game(self.current_language)
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
        self.show_frame(ScoreScreen).update(score, total, self.current_language)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.set_buttons(cont)
        return frame
    
    def set_buttons(self, cont):
        if cont == StartScreen:
            self.buttons.set_all(self.wrap_call(self.start_game))
            self.buttons.set(4, self.wrap_call(lambda: self.next_language()))
        elif cont == QuestionScreen:
            self.buttons.set(0, self.wrap_call(self.restart_game))
            self.buttons.set(1, self.wrap_call(lambda: self.check_answer(0)))
            self.buttons.set(2, self.wrap_call(lambda: self.check_answer(1)))
            self.buttons.set(3, self.wrap_call(lambda: self.check_answer(2)))
            self.buttons.set(4, self.wrap_call(lambda: self.check_answer(3)))
        elif cont == ScoreScreen:
            self.buttons.set_all(self.wrap_call(self.restart_game))
        else:
            raise ValueError("No such screen")
    
    def wrap_call(self, callback):
        return lambda: self.after(0, callback)
    
    def next_language(self):
        if self.current_language == 'estonian':
            self.current_language = 'english'
        else:
            self.current_language = 'estonian'

        self.frames[StartScreen].set_language(self.current_language)

app = QuizApp()
app.mainloop()