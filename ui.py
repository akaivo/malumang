import tkinter as tk

from reactivex import Subject

PADDING = 10
BG = "green"

class StartScreen(tk.Frame):
    def __init__(self, parent, controller, start_subject, answer_subject):
        tk.Frame.__init__(self, parent, bg=BG)
        start_button = tk.Button(
            self, text="Alusta mängu!",
            command=lambda: start_subject.on_next(None),
            relief=tk.FLAT
        )
        start_button.place(
            x=PADDING,
            y=PADDING,
            width=parent.winfo_width() - 2*PADDING,
            height=parent.winfo_height() - 2*PADDING
        )

class QuestionScreen(tk.Frame):
    def __init__(self, parent, controller, start_subject, answer_subject):
        tk.Frame.__init__(self, parent, bg=BG)
        self.question_label = tk.Label(self, text="Küsimus", bg='white')
        self.question_label.place(
           x=PADDING,
           y=PADDING,
           height=parent.winfo_height() * 0.75 - 2 * PADDING,
           width=parent.winfo_width() - 2 * PADDING
        )

        answers = tk.Frame(self, bg=BG)
        answers.place(
           x=PADDING,
           y=parent.winfo_height() * 0.75,
           height=parent.winfo_height() * 0.25 - PADDING,
           width=parent.winfo_width() - 2 * PADDING)

        w = parent.winfo_width() - 2 * PADDING
        h = parent.winfo_height() * 0.25 - PADDING
        x = 0.5 * w + 0.5 * PADDING
        y = 0.5 * h + 0.5 * PADDING

        self.answer_1 = tk.Label(answers, text=f"Vastus 1", bg='white')
        self.answer_1.bind('<Button-1>', lambda _: answer_subject.on_next(1))
        self.answer_1.place(x=0, y=0, height=0.5*(h - PADDING), width=0.5*(w - PADDING))

        self.answer_2 = tk.Label(answers, text=f"Vastus 2", bg='white')
        self.answer_2.bind('<Button-1>', lambda _: answer_subject.on_next(2))
        self.answer_2.place(x=(0.5*w + 0.5*PADDING), y=0, height=0.5*(h - PADDING), width=0.5*(w - PADDING))

        self.answer_3 = tk.Label(answers, text=f"Vastus 3", bg='white')
        self.answer_3.bind('<Button-1>', lambda _: answer_subject.on_next(3))
        self.answer_3.place(x=0, y=(0.5*h + 0.5*PADDING), height=0.5*(h - PADDING), width=0.5*(w - PADDING))

        self.answer_4 = tk.Label(answers, text=f"Vastus 4", bg='white')
        self.answer_4.bind('<Button-1>', lambda _: answer_subject.on_next(4))
        self.answer_4.place(x=(0.5*w + 0.5*PADDING), y=(0.5*h + 0.5*PADDING), height=0.5*(h - PADDING), width=0.5*(w - PADDING))
    
    def fill_question(self, question):
        self.question_label.configure(text=question["question"])
        self.answer_1.configure(text=question["answers"][0])
        self.answer_2.configure(text=question["answers"][1])
        self.answer_3.configure(text=question["answers"][2])
        self.answer_4.configure(text=question["answers"][3])


class ScoreScreen(tk.Frame):
    def __init__(self, parent, controller, start_subject, answer_subject):
        tk.Frame.__init__(self, parent, bg=BG)
        score_label = tk.Label(self, text="Sinu punktid: 10/10 !")
        score_label.place(
            x=PADDING,
            y=PADDING,
            width=parent.winfo_width() - 2*PADDING,
            height=parent.winfo_height() - 2*PADDING
        )
        score_label.bind("<Button-1>", lambda x: controller.show_frame(StartScreen))


class QuizApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.start_subject = Subject()
        self.restart_subject = Subject()
        self.answer_subject = Subject()

        self.attributes("-fullscreen", True)
        self.bind('<Escape>', lambda x: self.destroy())
        self.bind('1', lambda _: self.restart_subject.on_next(None))

        self.frames = {}
        for F in (StartScreen, QuestionScreen, ScoreScreen):
            frame = F(
                parent=self,
                controller=self,
                start_subject=self.start_subject,
                answer_subject=self.answer_subject
            )
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.show_frame(StartScreen)

    def display_question(self, question):
        self.show_frame(QuestionScreen).fill_question(question)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        return frame