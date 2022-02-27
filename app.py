import tkinter as tk
from tkinter import ttk
from frames import Main_window, New_entry, Edit_entry


COLOUR_PRIMARY = "#546E7A"
COLOUR_SECONDARY = "#37474F"
COLOUR_LIGHT_BACKGROUND = "#fff"
COLOUR_LIGHT_TEXT = "#eee"
COLOUR_DARK_TEXT = "#B0BEC5"

class Biudzetas(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Timer.TFrame", background=COLOUR_LIGHT_BACKGROUND)
        style.configure("Background.TFrame", background=COLOUR_PRIMARY)
        style.configure(
            "TimerText.TLabel",
            background=COLOUR_LIGHT_BACKGROUND,
            foreground=COLOUR_DARK_TEXT,
            font="Courier 24"
        )

        style.configure(
            "LightText.TLabel",
            background=COLOUR_PRIMARY,
            foreground=COLOUR_LIGHT_TEXT,
        )

        style.configure(
            "Button.TButton",
            background=COLOUR_SECONDARY,
            foreground=COLOUR_LIGHT_TEXT,
        )

        style.map(
            "Button.TButton",
            background=[("active", COLOUR_PRIMARY), ("disabled", COLOUR_LIGHT_TEXT)]
        )

        self["background"] = COLOUR_PRIMARY

        self.title("Biudžetas")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        container = ttk.Frame(self)
        container.grid()
        container.columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Main_window, New_entry, Edit_entry):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main_window)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

app = Biudzetas()
app.mainloop()
