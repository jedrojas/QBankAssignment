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
from socket import timeout

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


def saveobj(obj, nof):
    nameOfFile = nof
    obj = json.dumps(obj)
    with open(nameOfFile, 'w') as f:
        json.dump(obj, f, ensure_ascii=False)


def loadobj(nof):
    nameOfFile = nof
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


def makeContestConnection(cnum, usernameDict, contestants):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 0))
    global port
    port = s.getsockname()[1]
    print("Contest " + str(cnum) + " started on port " + str(port))
    s.listen(5)
    try:
        s.settimeout(10)
        while True:
            c, addr = s.accept()
            contestants.append(c)
            sendData = ("Joined server, waiting for contest to begin!")
            sendData = json.dumps(sendData)
            c.send(sendData.encode())
    except:
        print("contest entry over, beginning contest!")
    begincontest(contestants, usernameDict, cnum)


def begincontest(contestants, usernameDict, cnum):
    nameholder = []
    stats = {}
    questioncount = 0

    gathernicknames(contestants, usernameDict, nameholder)
    for name in nameholder:
        stats.update({name: 0})

    # while hasmorequestions(cnum):
    #     givenextquestion(contestants)

        # HERE:
        # while loop to go through questions in contest
        # for key, value in stats.items():
        #     print(key)
        #     print(value)
        # givequestions()

        # def givequestions()


def gathernicknames(contestants, usernameDict, nameholder):
    threads = []
    for c in contestants:
        t = Thread(target=getnickname, args=[
                   c, usernameDict, contestants, nameholder])
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()


def getnickname(c, usernameDict, contestants, nameholder):
    sendData = ("Please input a nickname: ")
    sendData = json.dumps(sendData)
    c.send(sendData.encode())

    nametaken = True
    while nametaken:
        rcvdData = c.recv(1024).decode()
        temp = json.loads(rcvdData)
        if temp in usernameDict:
            sendData = ("Error: nickname taken! Please enter another")
            sendData = json.dumps(sendData)
            c.send(sendData.encode())
        else:
            usernameDict.update({temp: temp})
            save_name(usernameDict)
            nameholder.append(temp)
            sendData = ("Hello " + temp + "! Welcome to the contest")
            sendData = json.dumps(sendData)
            c.send(sendData.encode())
            nametaken = False


def connectuser(c, usernameDict):
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


def getdatafromjson(nof):
    someDict = {}
    try:
        someDict = loadobj(nof)
        if type(someDict) == str:
            someDict = {}
    except (OSError, IOError, EOFError) as e:
        someDict = json.dumps({})
        saveobj(someDict, nof)
        someDict = {}
    return someDict


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
                    # create contest
                    getdatafromjson(nameOfFile)
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
                        contestDict = getdatafromjson(nameOfFile)
                        contestDict.update({qnumber: questionDict[qnumber]})
                        saveobj(contestDict, nameOfFile)

            # for key, value in temp.items():
            #     questionDict.update({key: value})

                        sendData = ("Added question " + qnumber +
                                    " to contest " + cnumber)
                    else:
                        sendData = ("Error: Question " +
                                    qnumber + " does not exist")
            except (OSError, IOError, EOFError) as e:
                sendData = ("Error: Contest " + cnumber + " does not exist")
            sendData = json.dumps(sendData)
        elif tempfirst == "b":
            contestants = []
            temprest = temprest.strip(" ")
            contestnum = temprest
            try:
                nameOfFile = "contest" + contestnum + ".txt"
                with open(nameOfFile) as json_file:
                    sendData = ("contest can be started")
                    _thread.start_new_thread(
                        makeContestConnection, (contestnum, usernameDict, contestants))
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
