from tkinter.filedialog import *
from tkinter.ttk import Combobox
import time
from time import gmtime, strftime
from threading import Thread

from erebor import IO
from Train import *

trains = list()
height = 300
filepath = "trains.txt"
runningText = "УВАЖАЕМЫЕ ПАССАЖИРЫ! НЕ ЗАБЫВАЙТЕ СВОИ ВЕЩИ В ПОЕЗДАХ И НА ВОКЗАЛЕ!"
inputTrainsInfo = IO.fileToList(filepath)
stations = ["Новая деревня", "Лахта", "Ольгино", "Горская", "Александровская", "Разлив", "Сестрорецк"]

def sync(lst):
    global inputTrainsInfo
    global filepath
    IO.listToFile(filepath, lst)
    inputTrainsInfo = IO.fileToList(filepath)

text = None
pause = False

def saveConfig():
    global text
    lst = text.get(1.0, END).strip().split("\n")
    for i in range(0, len(lst)):
        lst[i] = lst[i].split()
    sync(lst)
    for widget in timetable.winfo_children():
        widget.destroy()
    drawTimetable()
    drawStations()
    drawinputTrainsInfo()
    drawLabels()
    setMinutes()
    height = 200 + len(inputTrainsInfo) * 20
    root.geometry("800x" + str(height))

def showConfig():
    global inputTrainsInfo
    global text
    config = Tk()
    config.title("Конфигурация расписания")
    config.geometry("400x150")
    config.resizable(0, 0)

    configbar = Menu(config)
    configMenu = Menu(configbar, tearoff=0)
    configMenu.add_command(label="Сохранить", command=saveConfig)

    configbar.add_cascade(label="Файл", menu=configMenu)
    text = Text(config, height=8, width=35)
    for i in range(1, len(inputTrainsInfo) + 1):
        text.insert(END, inputTrainsInfo[i - 1])
        text.insert(END, "\n")
        label = Label(config, text="Электропоезд №" + str(i), font="Arial 8", fg='#333')
        label.place(x=7, y=(i - 1) * 16 + 9)
    text.pack(side='right')
    config.config(menu=configMenu)
    config.update()

def clock():
    global currentTime
    while (1):
        currentTime.set(strftime("%Y-%m-%d %H:%M", gmtime()))
        root.update()
        time.sleep(1)

def setPause():
    global pause
    pause = not pause

def runRow():
    global dots
    runLabel = Label(root, textvariable=dots, font=('Perfograma', 11), bg='#333633', fg='#9f9')
    runLabel.pack(side='bottom', fill='x')
    while (1):
        if (pause == False):
            if (len(dots.get()) * 0.8 > root.winfo_width()): dots.set(" " * 300 + runningText)
            dots.set(dots.get() + " ")
            root.update()
        time.sleep(0.02)

def quit(event):
    global root
    root.destroy()

def loadFile():
    fn = askopenfile(root, filetypes=[('Текстовые документы', '*.txt'), ('All files', '*')])

def calculate():
    print(len(trains))
    txt = "До указанной станции поезд не идет"
    min = 999
    minTrain = list()
    ind = stations.index(cb.get()) + 1
    for train in trains:
        if (ind in train.getStations()):
            try:
                if (float(train.getMinutes()[ind - 1]) < float(min)):
                    minTrain.clear()
                    min = train.getMinutes()[ind - 1]
                if (float(train.getMinutes()[ind - 1]) == float(min)):
                    minTrain.append(trains.index(train) + 1)
            except:
                IndexError

    if (len(minTrain) == 1):
        txt = "Минимальное время в пути составит " + str(min) + " минут на поезде №" + str(minTrain)
    if (len(minTrain) > 1):
        txt = "Минимальное время в пути составит " + str(min) + " минут на поездах №" + str(minTrain)
    txt = re.sub(r"[\[\]]", "", txt)
    label = Label(ticketFrame, text=txt)
    label.grid(row=1, column=4)

root = Tk()
root.title("Расписание электричек")
root.geometry("800x" + str(height))
root.resizable(0, 0)
currentTime = StringVar()
dots = StringVar()
dots.set(" " * 300 + runningText)
timetable = Frame(root, height=200, bg='#333633')

def drawTimetable():
    timetable.pack(side='top', fill='x')

drawTimetable()

def setMinutes():
    trains.clear()
    for i in range(0, len(inputTrainsInfo)):
        train = Train(inputTrainsInfo[i])
        trains.append(train)
    for i in range(0, len(trains)):
        for j in range(0, len(stations)):
            try:
                label = Label(timetable, text=re.sub("None", "", str(trains[i].getMinutes()[j])),
                              font=('Perfograma', 11), bg='#333633', fg='#9f9')
                label.grid(row=3 + i, column=2 + j)
            except:
                IndexError
setMinutes()

def drawLabels():
    mainLabel = Label(timetable, text="Расписание поездов", font=('Perfograma', 9), bg='#333633', fg='#9f9')
    mainLabel.grid(row=1, column=2, columnspan=5)

    timeLabel = Label(timetable, textvariable=currentTime, font=('Perfograma', 11), bg='#333633', fg='#9f9')
    timeLabel.grid(row=2, column=2 + len(stations))

    label = Label(timetable, text="Поезда:", font=('Perfograma', 9), bg='#333633', fg='#9f9')
    label.grid(row=2, column=1)


drawLabels()

def drawStations():
    for i in range(0, len(stations)):
        label = Label(timetable, text=stations[i], font=('Perfograma', 7), bg='#333633', fg='#9f9')
        label.grid(row=2, column=2 + i)

drawStations()

def drawinputTrainsInfo():
    for i in range(1, len(inputTrainsInfo) + 1):
        label = Label(timetable, text="Электропоезд №" + str(i), font=('Perfograma', 13), bg='#333633', fg='#9f9')
        label.grid(row=2 + i, column=1, pady=5, padx=5)

drawinputTrainsInfo()

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Текущая конфигурация", command=showConfig)

menubar.add_cascade(label="Файл", menu=filemenu)

runbar = Menu(root)
runmenu = Menu(runbar, tearoff=0)
runmenu.add_command(label="Пауза", command=setPause)

menubar.add_cascade(label="Бегущая строка", menu=runmenu)

ticketFrame = Frame(root, width=200, height=400, bg='#ded', bd=2)
ticketFrame.pack(side='bottom', fill='x', expand=True)

label = Label(ticketFrame, text="Выберите станцию", bg='#ded')
label.grid(row=1, column=1)

cb = Combobox(ticketFrame, values=stations, height=80)
cb.grid(row=1, column=2)

btn = Button(ticketFrame, text="Рассчитать", command=calculate)
btn.grid(row=1, column=3)

root.config(menu=menubar)
thread = Thread(target=clock)
thread.start()

thread = Thread(target=runRow)
thread.start()

root.mainloop()
