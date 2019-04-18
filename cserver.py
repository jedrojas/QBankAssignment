# Allison Kahn edit
# CNT4007C
# Project 1
# Code based on https://stackoverflow.com/questions/21233340/sending-string-via-socket-python
#!/usr/bin/env python3
import socket
import json
import random
import _thread
from threading import Timer
from threading import Thread
import time
import multiprocessing

# TODO
# input validation on s, b


def save_obj(obj, name):
    nameOfFile = "qbank.txt"
    obj = json.dumps(obj)
    with open(nameOfFile, 'w') as f:
        json.dump(obj, f, ensure_ascii=False)


def load_obj(name):
    nameOfFile = "qbank.txt"
    with open(nameOfFile) as json_file:
        file = json.load(json_file)
        return json.loads(file)


def save_name(name):
    nameOfFile = "usernamebank.txt"
    name = json.dumps(name)
    with open(nameOfFile, 'w') as f:
        json.dump(name, f, ensure_ascii=False)


def load_names():
    nameOfFile = "usernamebank.txt"
    with open(nameOfFile) as json_file:
        file = json.load(json_file)
        return json.loads(file)


def firstmakeConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 0))
    global port
    port = s.getsockname()[1]
    print(port)
    s.listen(5)
    c, addr = s.accept()
    return c


def makeConnection():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', port))
    print(port)
    s.listen(5)
    c, addr = s.accept()
    return c


def makeContestConnection(cnum, usernameDict):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 0))
    global port
    port = s.getsockname()[1]
    print("Contest " + str(cnum) + " started on port " + str(port))
    s.listen(5)
    # set timer here
    # timeout = time.time() + 5
    # t = Timer(5, timeout, [s])
    # t.start()
    # t.join()
    while True:
        c, addr = s.accept()
        _thread.start_new_thread(runcontest, (c, usernameDict))

    # t = Thread(target=acceptconnections)
    # t2 = Thread(target=closeT(), args=[t])
    s.close()


# def acceptconnections(n, c, s, usernameDict):
#     while True:
#         c, addr = s.accept()
#         _thread.start_new_thread(runcontest, (c, usernameDict))


# def closeT(t):
#     timeout = time.time() + 5
#     while time.time() < timeout:
#         # do nothing
#         # t.close()


# def timeout(s):
#     if s.sock_conn is None:
#         s.connect(s.socket_name)
#     print("game over")


def hello():
    print("hello")


# def on_new_client(clientsocket, addr):
#     while True:
#         sendData = ("Please input a nickname: ")
#         msg = clientsocket.recv(1024)
#         # do some checks and if msg == someWeirdSignal: break:
#         msg = input('SERVER >> ')
#         # Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
#         clientsocket.send(msg)
#     clientsocket.close()


def runcontest(c, usernameDict):

    # don't think I need this while loop
    while True:
        rcvdData = c.recv(1024).decode()
        if rcvdData != "":
            temp = json.loads(rcvdData)
            usernameDict = load_names()
            if type(usernameDict) == str:
                usernameDict = {}
            if temp in usernameDict:
                sendData = ("Error: username " + temp + " already taken.")
            else:
                # add username to dict, then save dict
                usernameDict.update({temp: temp})
                save_name(usernameDict)
                # usernameDict = load_names()
                sendData = ("Hello " + temp + "! Get ready for the contest!")

            sendData = json.dumps(sendData)
        else:
            sendData = "Error: No input given"
        c.send(sendData.encode())


c = firstmakeConnection()
questionDict = {}
usernameDict = {}

try:
    questionDict = load_obj("questions")
    if type(questionDict) == str:
        questionDict = {}
except (OSError, IOError, EOFError) as e:
    questionDict = json.dumps({})
    save_obj(questionDict, "questions")
    questionDict = {}

try:
    usernameDict = load_names()
    if type(usernameDict) == str:
        usernameDict = {}
except (OSError, IOError, EOFError) as e:
    usernameDict = json.dumps({})
    save_name(usernameDict)
    usernameDict = {}

while True:
    rcvdData = c.recv(1024).decode()
    if rcvdData != "":
        temp = json.loads(rcvdData)
        tempfirst = ""
        if type(temp) != dict:
            tempfirst = temp[:1]
            temprest = temp[1:]

        if temp == "Nothing to send":

            sendData = ""
        elif temp == "End server":
            break
        elif temp == "Ending client":
            c.close()
            c = makeConnection()
            sendData = ""
            sendData = json.dumps(sendData)
        elif type(temp) == dict:
            for key, value in temp.items():
                questionDict.update({key: value})
            save_obj(questionDict, "questions")
            sendData = json.dumps("")
        elif temp == "GetDict":
            sendData = json.dumps(questionDict)

        elif tempfirst == "p":
            temprest = temprest.strip(" ")
            if temprest in questionDict:
                sendData = ("Error: question number " +
                            temprest + " already used.")
            else:
                sendData = temprest
            sendData = json.dumps(sendData)

        elif tempfirst == "d":
            temprest = temprest.strip(" ")
            if temprest in questionDict:
                sendData = ("Deleted question " + temprest)
                questionDict.pop(temprest)
            else:
                sendData = (temprest + " is not available to delete")
            sendData = json.dumps(sendData)
        elif tempfirst == "g":
            temprest = temprest.strip(" ")
            if temprest in questionDict:
                sendData = questionDict[temprest]
            else:
                sendData = ("Error: question " + temprest + " not found")
            sendData = json.dumps(sendData)
        elif tempfirst == "r":
            if bool(questionDict) == False:
                sendData = "None"
            else:
                sendData = random.choice(list(questionDict.items()))
            sendData = json.dumps(sendData)
        elif tempfirst == "c":
            temprest = temprest[1:]
            qnumber = temprest.split(" ")[0]
            answer = temprest.split(" ")[1]
            if qnumber in questionDict:
                if questionDict[qnumber][3] == answer:
                    sendData = "Correct"
                else:
                    sendData = "Incorrect"
            else:
                sendData = "Question not entered"
            sendData = json.dumps(sendData)
        elif tempfirst == "s":
            temprest = temprest.strip(" ")
            contestnum = temprest
            if contestnum != "":
                try:
                    nameOfFile = "contest" + contestnum + ".txt"
                    with open(nameOfFile) as json_file:
                        sendData = ("Error: Contest " +
                                    contestnum + " already exists")
                except (OSError, IOError, EOFError) as e:
                    sendData = contestnum
                sendData = json.dumps(sendData)
            else:
                sendData = ("Error: invalid input")
        elif tempfirst == "a":
            temprest = temprest[1:]
            cnumber = temprest.split(" ")[0]
            qnumber = temprest.split(" ")[1]
            try:
                nameOfFile = "contest" + cnumber + ".txt"
                with open(nameOfFile) as json_file:
                    if qnumber in questionDict:
                        sendData = ("Added question " + qnumber +
                                    " to contest " + cnumber)
                    else:
                        sendData = ("Error: Question " +
                                    qnumber + " does not exist")
            except (OSError, IOError, EOFError) as e:
                sendData = ("Error: Contest " + cnumber + " does not exist")
            sendData = json.dumps(sendData)
        elif tempfirst == "b":
            temprest = temprest.strip(" ")
            contestnum = temprest
            try:
                nameOfFile = "contest" + contestnum + ".txt"
                with open(nameOfFile) as json_file:
                    sendData = ("contest can be started")
                    _thread.start_new_thread(
                        makeContestConnection, (contestnum, usernameDict))
                    # /conn = makeContestConnection(contestnum)
            except (OSError, IOError, EOFError) as e:
                sendData = ("contest cannot be started")
            sendData = json.dumps(sendData)

        else:
            # print("It's a dict")
            print("")
    else:
        sendData = json.dumps("")

    c.send(sendData.encode())
    save_obj(questionDict, "questions")


c.close()
