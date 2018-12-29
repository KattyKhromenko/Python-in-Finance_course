# -*- coding: utf-8 -*-

# Для выполнения кода необходимо установить библиотеки reportlab и tkinter. thinter через pip install в командной строке не устанавливается, поэтому необходимо
#установить thinker при загрузке Python в версии 3.5.1.

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# for graphic user interface
from Tkinter import *
from tkFileDialog import askopenfilename, askdirectory
from tkMessageBox import showerror

import os
import csv

root = None

 #1а-b  В рамках данного фрагмента кода использовались картинка и таблица, полученные по результатам 2 самостоятельного задания.
 #Таблица должна быть сохранена в формате csv, картинка - в png. Также пользователь указывает путь в директорию, в которую должны быть сохранены
 #все файлы. Для этого использовалась картинка объема на лучших ценах покупки и продажи в задании №2 и таблица стакана.

# put filenames in list in order to scale
csv_files = []
png_files = []
output_dir = ""
OUTPUTFILE_DEFAULT = "report.pdf"
output_file = ""

def browseFile():
    filename = askopenfilename()
    if filename.endswith('csv'):
        csv_files.append(filename)
    elif filename.endswith('png'):
        png_files.append(filename)
    else:
        showerror('Error', 'file %s has unsupported extension' % filename)

def browseDir():
    # global special word in order to be able to change variables from global scope
    global output_dir
    output_dir = askdirectory()
    print (output_dir)

def validate_input():
    if len(csv_files) == 0:
        showerror('Error', 'no csv file is provided')
    if len(png_files) == 0:
        showerror('Error', 'no png file is provided')
    global output_file
    if not output_file:
        output_file = OUTPUTFILE_DEFAULT

#c.ii.2. Ликвидность
#Данный фрагмент кода генерирует отчет о результатах расчетов по заданным параметрам. Отчет генерируется в формате pdf.
def readCSV(file_name):
    with open(file_name, 'rU') as f:  # opens PW file
        return list(list(rec) for rec in csv.reader(f, delimiter=','))

def generate():
    validate_input()
    pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
    print(os.path.join(output_dir, output_file))
    canv = canvas.Canvas(os.path.join(output_dir, output_file), pagesize=letter)
    canv.setLineWidth(.3)
    canv.setFont('FreeSans', 32)
    canv.drawCentredString(300, 750, u'Отчет')
    canv.setFont('FreeSans', 12)
    canv.drawString(30, 725, 'Данный отчет содержит объем на лучших ценах покупки и продажи и стакан')

#c.iv. График и таблица
    # adjust here x, y, width and height - для пользователя
    canv.drawImage(png_files[0], 100, 500, width=300, height=200)
    canv.drawString(50, 490, 'На графике представлено')

    data = readCSV(csv_files[0])
    t = Table(data)
    t.wrapOn(canv, 0, 0)
    t.setStyle(TableStyle(
        [('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
         ('BOX', (0,0), (-1,-1), 0.25, colors.black)
         ]
    )
    )
    t.drawOn(canv, 30, 300)
    canv.drawString(50, 290, 'В таблице представлено')
    canv.save()
    root.destroy()

# Function that draws user interface

def addLabel(text, row):
    labelText = StringVar()
    labelText.set(text)
    label = Label(root, height=5, textvariable=labelText)
    label.grid(row=row, column=0)

def buttonFile(text, row):
    addLabel(text, row)
    browsebutton = Button(root, width=10, text="Browse", command=browseFile)
    browsebutton.grid(row=row, column=1)

def buttonDir(text, row):
    addLabel(text, row)
    browsebutton = Button(root, width=10, text="Browse", command=browseDir)
    browsebutton.grid(row=row, column=1)

def entryFileName(text, row):
    addLabel(text, row)
    directory = StringVar(None)
    output_entry = Entry(root, textvariable=directory)
    output_entry.grid(row=row, column=1)
    global output_file
    output_file = output_entry.get()

def actionButton(row):
    browsebutton = Button(root, width=5, text="Generate", command=generate)
    browsebutton.grid(row=row, column=1)


def startApplication():
    global root
    root = Tk()
    buttonFile('Browse path to picture', row=0)
    buttonFile('Browse path to table', row=1)
    buttonDir('Browse path to output directory', row=2)
    entryFileName('Enter output file', row=3)

    actionButton(row=4)
    mainloop()


startApplication()

# csv_files.append('files/random.csv')
# png_files.append('files/png.png')
# output_dir = 'output'
# output_file = 'report.pdf'
# generate()