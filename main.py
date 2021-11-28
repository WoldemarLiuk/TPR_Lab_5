from tkinter import *
import tkinter as tk

from scipy import optimize
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import numpy as np

root = Tk()

w = root.winfo_screenwidth()
h = root.winfo_screenheight()
w = w//2
h = h//2
w = w - 310
h = h - 225
root.geometry('600x420+{}+{}'.format(w, h))
root.title("Теорія ігор. Матричні ігри")

showinfo(
        title='Оберіть файл з матрицею',
        message='Будь ласка, оберіть файл з матрицею!'
    )

filetypes = (
    ('text files', '*.txt'),
    ('All files', '*.*')
)

filename = fd.askopenfilename(
    title='Відкрити файл',
    initialdir='/',
    filetypes=filetypes)

class Table:
    def __init__(self, root):
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=10, font=('Arial', 10))
                self.e.grid(row=i, column=j, padx=10, pady=10)
                self.e.insert(END, lst[i][j])

lst = np.loadtxt(filename, dtype='i', delimiter=',')

total_rows = len(lst)
total_columns = len(lst[0])
t = Table(root)

def count():

    lst = np.loadtxt(filename, dtype='i', delimiter=',')

    minimum = np.min(lst, axis=1)
    maximum = np.max(lst, axis=0)

    A_maxmin = np.max(minimum)

    B_minmax = np.min(maximum)

    if A_maxmin != B_minmax:
        no_point = "Сідлова точка відсутня! Ціна гри знаходиться в межах"

    lst_del = np.delete(lst, 0, 0)
    lst_del1 = np.delete(lst_del, 3, 0)
    lst_del2 = np.delete(lst_del1, 0, 1)
    lst_del3 = np.delete(lst_del2, 3, 1)
    lst_del4 = np.delete(lst_del3, 2, 1)
    lst_del5 = np.delete(lst_del4, 0, 0)

    #Симплекс метод
    func = [1, 1]

    left_part = [[-lst_del5[0, 0], -lst_del5[0, 1]],
                 [-lst_del5[1, 0], -lst_del5[1, 1]]]

    right_part = [-1, -1]

    bound = [(0, float("inf")),
             (0, float("inf"))]

    min = optimize.linprog(c=func, A_ub=left_part, b_ub=right_part,
                           bounds=bound,
                           method="simplex")
    res = round(1 / min.fun, 2)

    text1.delete("1.0", END)
    text1.insert("1.0", res)
    text1.insert("1.0", '\n\nЦіна гри розрахована симплекс-методом: ')
    text1.insert("1.0", lst_del5)
    text1.insert("1.0", '\nCпрощена матриця гри: \n')
    if A_maxmin != B_minmax:
        text1.insert("1.0", ']\n')
        text1.insert("1.0", B_minmax)
        text1.insert("1.0", '; ')
        text1.insert("1.0", A_maxmin)
        text1.insert("1.0", '[')
        text1.insert("1.0", no_point)
    text1.insert("1.0", '\n')
    text1.insert("1.0", B_minmax)
    text1.insert("1.0", '\nВерхня ціна гри: ')
    text1.insert("1.0", A_maxmin)
    text1.insert("1.0", 'Нижня ціна гри: ')
    text1.insert("1.0", 'Визначення сідлової точки:\n')

labelframe = LabelFrame(root, text="Розв'язок", width=580, height=190)
labelframe.place(x=10, y=205)

text1 = tk.Text(width=70, height=10)
text1.place(x=15, y=225)

b1 = tk.Button(text="Обчислити", command=count).place(x=495, y=85)

root.mainloop()