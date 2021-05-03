import tkinter
import socket
from tkinter import *

#Client side socket
PORT = 50000
SERVER = socket.gethostbyname(socket.gethostname())
address = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)

def send(msg):
    message = msg.encode('utf-8')
    msg_length = len(message)
    send_length = str(msg_length).encode('utf-8')
    send_length += b' ' * (64 - len(send_length))
    client.send(send_length)
    client.send(message)
    reply = client.recv(10).decode()
    update(reply)

def clicked():
    send(SAT_INPUT.get())
    send(GPA_INPUT.get())

def update(name):
    l_new = Label(window, text = name, font = ("ArialBold", 20))
    l_new.grid(column = 0, row = 3)

window = tkinter.Tk()
window.title('University Predictor')
SAT_INPUT = Entry(window, width = 10)
l1 = Label(window, text = "Sat score: ", font = ("ArialBold", 15))
GPA_INPUT = Entry(window, width = 10)
l2 = Label(window, text = "GPA : ", font = ("ArialBold", 15))
bt = Button (window, text= "Enter", command = clicked)
SAT_INPUT.grid(column = 1, row = 0)
l1.grid(column = 0, row = 0)
l2.grid(column = 0, row = 1)
GPA_INPUT.grid(column = 1, row = 1)
bt.grid(column = 0, row = 2)

window.mainloop()

