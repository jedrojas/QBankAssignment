# Allison Kahn edit
# CNT4007C
# Project 1
# Code based on https://stackoverflow.com/questions/21233340/sending-string-via-socket-python
#!/usr/bin/env python3
import socket
import json
import random


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


c = firstmakeConnection()
questionDict = {}

try:
    questionDict = load_obj("questions")
    if type(questionDict) == str:
        questionDict = {}
except (OSError, IOError, EOFError) as e:
    questionDict = json.dumps({})
    save_obj(questionDict, "questions")
    questionDict = {}


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
        # elif temp == "GetNextQNum":
            # for x in range(1, 500):
            #     x = str(x)
            #     if x not in questionDict:
            #         questionNum = x
            #         break

            # sendData = json.dumps(questionNum)
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
                print("trying number: " + contestnum)

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

        else:
            # print("It's a dict")
            print("")
    else:
        sendData = json.dumps("")

    c.send(sendData.encode())
    save_obj(questionDict, "questions")


c.close()
