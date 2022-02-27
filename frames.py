import re
import tkinter as tk
from tkinter import ttk
from tkinter import *
from db import engine, Biudzeto, Base
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

class Main_window(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.bind("<<ShowFrame>>", lambda e: self.update_list())

        self["style"] = "Background.TFrame"

        self.balansas = tk.StringVar()
        self.pajamos = tk.StringVar()
        self.islaidos = tk.StringVar()

        income = ttk.Label(self, text="Pajamų suma: ", style="LightText.TLabel")
        income.grid(row=0, column=0, sticky="W", padx=(10, 0), pady=(10, 0))
        incomesum = ttk.Label(self, textvariable=self.pajamos, style="TimerText.TLabel")
        incomesum.grid(row=0, column=1, sticky="W", padx=(10, 0), pady=(10, 0))

        expence = ttk.Label(self, text="Išlaidų suma: ", style="LightText.TLabel")
        expence.grid(row=1, column=0, sticky="W", padx=(10, 0), pady=(10, 0))
        expencesum = ttk.Label(self, textvariable=self.islaidos, style="TimerText.TLabel")
        expencesum.grid(row=1, column=1, sticky="W", padx=(10, 0), pady=(10, 0))

        balance = ttk.Label(self, text="Balansas", style="LightText.TLabel")
        balancesum = ttk.Label(self, textvariable=self.balansas, style="TimerText.TLabel")
        balancesum.grid(row=2, column=1, sticky="EW", padx=10, pady=(10,0))
        balance.grid(row=2, column=0, sticky="EW", padx=10, pady=(10, 0))

        newentry_button = ttk.Button(
            self,
            text="Naujas įrašas",
            command=lambda: controller.show_frame(New_entry),
            style="Button.TButton",
            cursor="hand2"
        )

        newentry_button.grid(row=0, column=2, sticky="E", padx=10, pady=(10,0))

        self.deleteentry_button = ttk.Button(
            self,
            text="Ištrinti įrašą",
            command=self.delete,
            style="Button.TButton",
            cursor="hand2",
            state="disabled"
        )
        self.deleteentry_button.grid(row=1, column=2, sticky="E", padx=10, pady=(10, 0))

        editentry_button = ttk.Button(
            self,
            text="Redaguoti įrašą",
            command=lambda: controller.show_frame(Edit_entry),
            style="Button.TButton",
            cursor="hand2"
        )

        editentry_button.grid(row=2, column=2, sticky="nsew", padx=10, pady=(10, 0))

        scrollbar = Scrollbar(self)
        self.list_of_entries = Listbox(self, yscrollcommand=scrollbar.set)
        self.update_list()
        scrollbar.config(command=self.list_of_entries.yview)
        self.list_of_entries.bind("<Button-1>", self.switchButtonState)

        self.list_of_entries.grid(row=4, columnspan=3, sticky="EW", padx=10, pady=(10, 0))
        scrollbar.grid(row=4, column=4, sticky="SN")

    def update_list(self):
        self.deleteentry_button['state'] = tk.DISABLED
        list1 = session.query(Biudzeto).all()
        self.list_of_entries.delete(0,END)
        for item in list1:
            self.list_of_entries.insert(END, item)

        išlaidos = session.query(Biudzeto).filter_by(tipas="Išlaidos")
        islaidusuma=0
        for item in išlaidos:
            islaidusuma += item.suma

        pajamos = session.query(Biudzeto).filter_by(tipas="Pajamos")
        pajamusuma=0
        for item in pajamos:
            pajamusuma += item.suma

        skirtumas = pajamusuma - islaidusuma

        self.balansas.set(skirtumas)
        self.pajamos.set(pajamusuma)
        self.islaidos.set(-abs(islaidusuma))

    def delete(self):
        selected_item = self.list_of_entries.curselection()
        item = self.list_of_entries.get(selected_item)
        item_id = item.split(".")[0]
        to_edit = session.query(Biudzeto).get(item_id)
        session.delete(to_edit)
        session.commit()
        self.update_list()
        self.deleteentry_button['state'] = tk.DISABLED

    def switchButtonState(self, event):
        if (self.deleteentry_button['state'] == tk.DISABLED):
            self.deleteentry_button['state'] = tk.NORMAL
        else:
            self.deleteentry_button['state'] = tk.NORMAL



class New_entry(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self["style"] = "Background.TFrame"

        self.entry_type = tk.StringVar(self)
        self.suma = tk.StringVar(self)
        self.komentaras = tk.StringVar(self)

        self.options = ["Išlaidos", "Pajamos"]

        self.type_lb = ttk.Label(self, text="Tipas", style="LightText.TLabel")
        self.sum_lb = ttk.Label(self, text="Suma", style="LightText.TLabel")
        self.comment_lb = ttk.Label(self, text="Komentaras", style="LightText.TLabel")
        self.type_input = ttk.OptionMenu(self, self.entry_type, self.options[0], *self.options)
        self.sum_input = ttk.Entry(self, text=self.suma)
        self.comment_input = ttk.Entry(self,  text=self.komentaras)
        self.save_btn = ttk.Button(self,
            text="Išsaugoti",
            command=self.update_database,
            style="Button.TButton",
            cursor="hand2"
        )
        self.cancel_btn = ttk.Button(self,
            text="Grįžti",
            command=lambda: controller.show_frame(Main_window),
            style="Button.TButton",
            cursor="hand2"
        )
        self.status = ttk.Label(self, text="", relief=SUNKEN, anchor=W)
        self.cancel_btn.bind("<Button-1>", self.clean_status)

        self.type_lb.grid(row=0, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.sum_lb.grid(row=1, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.comment_lb.grid(row=2, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.type_input.grid(row=0, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.sum_input.grid(row=1, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.comment_input.grid(row=2, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.save_btn.grid(row=3, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.cancel_btn.grid(row=3, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.status.grid(row=4, columnspan=3, sticky="EW")

    def update_database(self):
        if bool(re.match(r'^[0-9]+(\.[0-9]+)*$',self.sum_input.get())) is True:
            irasas = Biudzeto(self.entry_type.get(), self.suma.get(), self.komentaras.get())
            session.add(irasas)
            session.commit()
            self.status["text"] = f"{self.entry_type.get()}: {self.suma.get()} - įtraukta į biudžetą"
            self.sum_input.delete(0, END)
            self.comment_input.delete(0, END)
        else:
            self.sum_input.delete(0, END)
            self.status["text"] = 'Sumos laukelyje veskite tik skaičius (be "-" ženklo)'

    def clean_status(self, event):
        self.status["text"] = ""


class Edit_entry(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self["style"] = "Background.TFrame"

        self.bind("<<ShowFrame>>", lambda e: self.update_list())

        self.entry_type = tk.StringVar(self)
        self.suma = tk.StringVar(self)
        self.komentaras = tk.StringVar(self)

        self.options = ["Išlaidos", "Pajamos"]

        self.type_lb = ttk.Label(self, text="Tipas", style="LightText.TLabel")
        self.sum_lb = ttk.Label(self, text="Suma", style="LightText.TLabel")
        self.comment_lb = ttk.Label(self, text="Komentaras", style="LightText.TLabel")
        self.type_input = ttk.OptionMenu(self, self.entry_type, self.options[0], *self.options)
        self.sum_input = ttk.Entry(self, text=self.suma)
        self.comment_input = ttk.Entry(self, text=self.komentaras)
        self.save_btn = ttk.Button(self,
                                   text="Išsaugoti",
                                   command=self.update_database,
                                   style="Button.TButton",
                                   cursor="hand2"
                                   )
        self.cancel_btn = ttk.Button(self,
                                     text="Grįžti",
                                     command=lambda: controller.show_frame(Main_window),
                                     style="Button.TButton",
                                     cursor="hand2"
                                     )
        self.status = ttk.Label(self, text="", relief=SUNKEN, anchor=W)
        scrollbar = Scrollbar(self)
        self.list = Listbox(self, yscrollcommand=scrollbar.set)
        self.update_list()

        self.type_lb.grid(row=1, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.sum_lb.grid(row=2, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.comment_lb.grid(row=3, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.type_input.grid(row=1, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.sum_input.grid(row=2, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.comment_input.grid(row=3, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.save_btn.grid(row=4, column=1, sticky="Ew", padx=10, pady=(10, 0))
        self.cancel_btn.grid(row=4, column=0, sticky="Ew", padx=10, pady=(10, 0))
        self.status.grid(row=5, columnspan=3, sticky="EW")
        self.list.grid(row=0, columnspan=3, sticky="EW", padx=10, pady=(10, 0))
        scrollbar.grid(row=0, column=4, sticky="SN")

        self.list.bind('<<ListboxSelect>>', self.on_select)
        self.cancel_btn.bind("<Button-1>", self.clean_status)

    def on_select(self, event):
        if self.list.curselection() != ():
            selected_item = self.list.curselection()
            item = self.list.get(selected_item)
            item_id = item.split(".")[0]
            to_edit = session.query(Biudzeto).get(item_id)
            self.sum_input.delete(0, END)
            self.comment_input.delete(0, END)
            self.sum_input.insert(END, f"{to_edit.suma}")
            self.comment_input.insert(END, f"{to_edit.comments}")

    def update_database(self):
        if self.list.curselection() != ():
            if bool(re.match(r'^[0-9]+(\.[0-9]+)*$',self.sum_input.get())) is True:
                selected_item = self.list.curselection()
                item = self.list.get(selected_item)
                item_id = item.split(".")[0]
                to_edit = session.query(Biudzeto).get(item_id)
                to_edit.tipas = self.entry_type.get()
                to_edit.suma = self.suma.get()
                to_edit.comments = self.komentaras.get()
                session.commit()
                self.sum_input.delete(0, END)
                self.comment_input.delete(0, END)
                self.update_list()
                self.status["text"] = 'Pakeitimai atlikti'
            else:
                self.sum_input.delete(0, END)
                self.status["text"] = 'Sumos laukelyje veskite tik skaičius (be "-" ženklo)'

    def update_list(self):
        list1 = session.query(Biudzeto).all()
        self.list.delete(0,END)
        for item in list1:
            self.list.insert(END, item)

    def clean_status(self, event):
        self.status["text"] = ""
