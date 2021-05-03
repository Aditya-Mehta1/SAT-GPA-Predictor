import socket
import threading
from sklearn.ensemble import RandomForestClassifier
import sqlite3
import numpy as np

PORT = 50000
SERVER = socket.gethostbyname(socket.gethostname())
address = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(address)

def handle_client(conn, addr):
    print("[NEW CONNECTION]: " + str(addr))
    connected = True
    while connected:
        a = list()
        for x in (0,1):
            msg_length = conn.recv(64).decode('utf-8')
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode('utf-8')
            a.append(msg)
        conn.send(make_prediction(a[0], a[1]))
        connected = False
    conn.close()

def make_prediction(Sat, Gpa):
    model = RandomForestClassifier()
    connect = sqlite3.connect('data.sqlite')
    cur = connect.cursor()
    cur.execute('SELECT SAT FROM CMU1')
    SAT = cur.fetchall()
    cur.execute('SELECT GPA FROM CMU1')
    GPA = cur.fetchall()
    cur.execute('SELECT Acceptance FROM CMU1')
    Acceptance = cur.fetchall()

    i = 0
    for x in Acceptance:
        Acceptance[i] = x[0]
        i = i+1
    lst = list()
    i= 0
    for x in SAT:
        y = GPA[i]
        i = i+1
        lst.append((x[0],y[0]))
    arr= np.array(lst)
    model.fit(arr, Acceptance)
    arr2 = np.array((Sat,Gpa))
    return model.predict(arr2.reshape(1,-1))

def start():
    server.listen()
    while True:
        print("Connected on: " + str(address))
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args= (conn, addr))
        thread.start()
        print("[ACTIVE CONNECTIONS]" + str(threading.active_count() - 1))


start()
