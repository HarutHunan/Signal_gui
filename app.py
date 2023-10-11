import numpy as np

from graph import GraphFrame, NavigationToolbar
from comp import *

import tkinter as tk
from tkinter import ttk, filedialog

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class App(tk.Tk):
    """
    Класс для создания главного окна приложения
    """

    def __init__(self):
        """
        Конструктор класса
        """
        super().__init__()
        self._started = 0
        self.title("Graph Illustration")
        self.geometry("1024x720")

        self.files = []

    def upload_file(self, entry):
        self.filename = filedialog.askopenfilename(initialdir="D:/Pythongui", title="Выберите файл",
                                                   filetypes=[('LAn10 (binary) files', '*.LAn10')])
        print(self.filename)
        entry.delete(0, tk.END)
        entry.insert(0, self.filename)

        # offset - начиная с какого байта читать файл, dtype - как интерпретировать прочитанные строки.
        # Размер uint16 - 2 байта, поэтому чтение файла происходит 2 байтовыми блоками.

        f = np.fromfile(self.filename, dtype='uint16', offset=4)
        f1 = np.zeros((2, int(f.shape[0] / 2)))
        f1[0] = f[::2]
        f1[1] = f[1::2]
        # self.files.append(f1)

        sig = Signal(f1)
        self.files.append(sig)

        if len(self.files) == 2:
            dphi = Compute_Phase(self.files[0], self.files[1])
            file = np.array([i.data for i in self.files])
            self.graph1.draw_graph(np.array(file)[:, 0, 100000:200000])
            self.graph2.draw_graph(np.vstack((np.absolute(self.files[0].Spectrum1), np.absolute(self.files[0].Spectrum1)))[:, 0:200])
            self.graph3.draw_graph(np.vstack((self.files[0].Phase, self.files[1].Phase)))

            c = 180 / np.pi
            self.info_label1.config(text = self.info_label1.cget("text") + "    " + f"{self.files[0].Phi * c :.4f}")
            self.info_label2.config(text = self.info_label2.cget("text") + "    " + f"{self.files[1].Phi * c:.4f}")
            self.info_label3.config(text = self.info_label3.cget("text") + "    " + f"{dphi * c: .6f}")


    def set_filter(self):
        pass

    def save_file(self):
        # Add your code to save the file here
        np.savetxt("spectrum.txt", self.files[0].Spectrum1.T, delimiter=",")
        np.savetxt("phase.txt", self.files[0].Phase.T, delimiter=",")
        pass

    def drawfront(self):

        self.header = ttk.Frame(self, padding=(3, 3), relief='solid')
        self.header.grid(row=0, column=0, columnspan=2, pady=(3, 3), sticky='nsew')

        self.headtitle = ttk.Label(self.header, text="Измерение УВПП", font=("Helvetica", 16))
        self.headtitle.pack(pady=(3, 3))

        # Left part of the window
        self.left_frame = ttk.Frame(self, padding=(3, 3), relief="solid")
        self.left_frame.grid(row=1, column=0, rowspan=3, padx=(3, 3), pady=(3, 3), sticky='nsew')

        # Graph areas
        self.graph1 = GraphFrame(self.left_frame)
        self.graph1.set_title("Графики сигналов")
        self.graph1.grid(row=0, column=0)

        self.graph2 = GraphFrame(self.left_frame)
        self.graph2.set_title("График спектра")
        self.graph2.grid(row=1, column=0)

        #
        self.graph3 = GraphFrame(self.left_frame)
        self.graph3.set_title("График разности фаз")
        self.graph3.grid(row=2, column=0)

        # Right part of the window
        self.right_frame = ttk.Frame(self, padding=(3, 3), relief="solid")
        self.right_frame.grid(row=1, column=1, padx=(5, 5), pady=(5, 5), sticky='nsew')

        # Upload section
        self.upload_section = ttk.Frame(self.right_frame, padding=(5, 5))
        self.upload_section.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky='nsew')

        self.upload_label = ttk.Label(self.upload_section, text="Загрузка референтных измерений", font=("TkDefaultFont", 11))
        self.upload_label.grid(row=0, column=0, pady=(5, 5), padx=(0, 5))

        self.upload_button1 = ttk.Button(self.upload_section, text="Загрузить",
                                         command=lambda: self.upload_file(self.upload_entry1))
        self.upload_button1.grid(row=1, column=0, pady=(5, 5), padx=(0, 5))

        self.upload_entry1 = ttk.Entry(self.upload_section)
        self.upload_entry1.grid(row=1, column=1, pady=(5, 5), padx=(5, 5))

        self.upload_label = ttk.Label(self.upload_section, text="Загрузка объектных измерений", font=("TkDefaultFont", 11))
        self.upload_label.grid(row=2, column=0, pady=(5, 5), padx=(0, 5))

        self.upload_button2 = ttk.Button(self.upload_section, text="Загрузить",
                                         command=lambda: self.upload_file(self.upload_entry2))
        self.upload_button2.grid(row=3, column=0, pady=(5, 5), padx=(0, 5))

        self.upload_entry2 = ttk.Entry(self.upload_section)
        self.upload_entry2.grid(row=3, column=1, pady=(5, 5), padx=(5, 5))

        # Option menus section
        self.option_menu_section = ttk.Frame(self.right_frame, padding=(5, 5))
        self.option_menu_section.grid(row=1, column=0, padx=(5, 5), pady=(5, 5), sticky='nsew')

        self.option_menu1_label = ttk.Label(self.option_menu_section, text="Настройка сигнала", font=("TkDefaultFont", 12, "bold"))
        self.option_menu1_label.grid(row=0, column=0, pady=(5, 5))

        self.option_menu1_label = ttk.Label(self.option_menu_section, text="Выбор фильтра по предаточной функции", font=("TkDefaultFont", 11))
        self.option_menu1_label.grid(row=1, column=0, pady=(5, 5))

        self.option_menu1 = ttk.Combobox(self.option_menu_section, values=["Фильтр Блекмена-Харриса", "Фильтр Баттерворта", "Фильтр Чебышева"], width=25)
        self.option_menu1.current(0)
        self.option_menu1.grid(row=2, column=0, pady=(5, 5), padx=(5, 5))

        self.option_menu2_label = ttk.Label(self.option_menu_section, text="Выбор типа фильтра", font=("TkDefaultFont", 11))
        self.option_menu2_label.grid(row=3, column=0, pady=(5, 5))

        self.option_menu2 = ttk.Combobox(self.option_menu_section, values=["Фильтр низких частот", "Фильтр высоких частот"], width=25)
        self.option_menu2.current(0)
        self.option_menu2.grid(row=4, column=0, pady=(5, 5), padx=(5,5))

        self.option_menu3_label = ttk.Label(self.option_menu_section, text="Выбор порядка фильтра", font=("TkDefaultFont", 11))
        self.option_menu3_label.grid(row=5, column=0, pady=(5, 5))

        self.option_menu3 = ttk.Spinbox(self.option_menu_section, from_=1, to=10, increment=1)
        self.option_menu3.grid(row=6, column=0, pady=(5, 5), padx=(5, 5))

        self.option_menu3_button = ttk.Button(self.option_menu_section, text="Настроить",
                                              command=lambda: self.set_filter())
        self.option_menu3_button.grid(row=6, column=1, padx=(0, 5), pady=(5, 5))

        # Info section
        self.info_section = ttk.Frame(self.right_frame, padding=(7, 7))
        self.info_section.grid(row=2, column=0, rowspan=3, columnspan = 2, pady=(7, 7))

        self.info_label1 = ttk.Label(self.info_section, text="Угол опорного сигнала: ", font=("TkDefaultFont", 11))
        self.info_label1.grid(row=0, column=0, padx=(7, 7), pady=(7, 7))
        # self.info_label1.pack(side = tk.LEFT)
        self.info_value1 = ttk.Label(self.info_section, text="", font=("TkDefaultFont", 11))
        # self.info_value1.grid(row=0, column=1, pady=(3, 3), padx=(0, 3))

        self.info_label2 = ttk.Label(self.info_section, text="Угол объектного сигнала: ", font=("TkDefaultFont", 11))
        self.info_label2.grid(row=1, column=0, padx=(7, 7), pady=(7, 7))
        self.info_value2 = ttk.Label(self.info_section, text="", font=("TkDefaultFont", 11))
        # self.info_value2.grid(row=1, column=1, pady=(3, 3), padx=(0, 3))

        self.info_label3 = ttk.Label(self.info_section, text="Разность фаз: ", font=("TkDefaultFont", 11))
        self.info_label3.grid(row=2, column=0, padx=(7, 7), pady=(7, 7))
        self.info_value3 = ttk.Label(self.info_section, text="", font=("TkDefaultFont", 11))
        # self.info_value3.grid(row=2, column=1, pady=(3, 3))

        # Save button section
        self.save_section = ttk.Frame(self.right_frame)
        self.save_section.grid(row=14, column=0, columnspan=2, pady=(5, 5))

        self.save_label = ttk.Label(self.save_section, text="Сохранить файл", font=("TkDefaultFont", 11))
        self.save_label.grid(row=0, column=0, padx=(5, 5), pady=(5, 5))

        self.save_box = ttk.Combobox(self.save_section, values=["csv"])
        self.save_box.current(0)
        self.save_box.grid(row=1, column=0, pady=(5, 5), padx=(5, 5))

        self.save_button = ttk.Button(self.save_section, text="Save File", command=self.save_file)
        self.save_button.grid(row=1, column=1, pady=(5, 0))

        # Make the frames expandable
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.left_frame.grid_rowconfigure((1, 2, 3), weight=1)
        self.right_frame.grid_rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), weight=1)
        self.right_frame.grid_columnconfigure((0,1), weight=1)

        self.mainloop()

    def start(self):
        if self._started == 0:
            self.drawfront()
        self._started = 1
