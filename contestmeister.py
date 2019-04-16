# Allison Kahn
# CNT4007C
# Project 1
# Code based on https://stackoverflow.com/questions/21233340/sending-string-via-socket-python
#!/usr/bin/env python3
import socket
import json
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    hostname = sys.argv[1]
    port = sys.argv[2]
except:
    print("Missing arguments. Closing.")
    exit()

try:
    s.connect((hostname, int(port)))
except EnvironmentError as exc:
    print("Cannot create connection. Closing.")
    s.close()
    exit()
qtype = ''
questionDict = {}


while qtype != '1':

    qtype = input("> ")

    qtypefirst = qtype[:1]
    qtyperest = qtype[1:]

    if qtypefirst == 'p':

        tags = ""
        tags = input("")
        # tags = tags.split(",")
        qtemp = ""
        question = ""
        while(qtemp != "."):
            qtemp = input("")
            question = question + qtemp
        question = question[:-1]
        listOfQ = []
        prevAnswer = "Temp"
        currAnswer = ""
        currAnswerTemp = " "
        counter = 0
        while counter < 1:
            while counter < 1:
                currAnswerTemp = input("")
                currAnswer = currAnswer + currAnswerTemp
                if currAnswer == ".":
                    counter = counter + 1
                if(currAnswerTemp == "."):
                    break
            currAnswer = currAnswer[:-1]
            if(currAnswer != ""):
                if counter == 0:
                    counter = 0
                else:
                    counter = counter - 1
                listOfQ.append(currAnswer)
                currAnswer = ""
            if len(listOfQ) < 2 and counter == 1:
                print("Must have at least 2 choices. Please enter another option.")
                counter = counter - 1
            currAnswerTemp = ""
        correctAnswer = input("")

        ###

        sendData = json.dumps(qtype)
        s.send(sendData.encode())
        rcvdData = s.recv(1024).decode()
        response = json.loads(rcvdData)
        if response[0:5] == "Error":
            print(response)
        else:
            ###

            tempQuestion = {}

            wholeQuestion = []
            wholeQuestion.append(tags)
            wholeQuestion.append(question)
            wholeQuestion.append(listOfQ)
            wholeQuestion.append(correctAnswer)
            tempQuestion[response] = wholeQuestion
            # print(questionNum)
            print("Question " + response + " added.")

            sendData = (tempQuestion)
            sendData = json.dumps(sendData)
            s.send(sendData.encode())
            rcvdData = s.recv(1024).decode()

    elif qtypefirst == 'd':
        sendData = json.dumps(qtype)
        s.send(sendData.encode())
        rcvdData = s.recv(1024).decode()
        response = json.loads(rcvdData)
        print(response)

    elif qtypefirst == 'g':

        sendData = json.dumps(qtype)
        s.send(sendData.encode())
        rcvdData = s.recv(1024).decode()
        response = json.loads(rcvdData)
        if response == '':
            rcvdData = s.recv(1024).decode()
            response = json.loads(rcvdData)
        if response[0:5] == "Error":
            print(response)
        elif type(response) == list:
            print(response[0])
            print(response[1])
            for choice in response[2]:
                print(choice)
            print(response[3])
        else:
            print("Unable to get question")

    elif qtypefirst == 'r':

        sendData = json.dumps(qtype)
        s.send(sendData.encode())
        rcvdData = s.recv(1024).decode()
        response = json.loads(rcvdData)

        if type(response) != list:
            print("There are no questions entered")
            qtype = "reset"
            continue
        else:
            number, info = response
            print(number)
            print(info[1])
            for x in info[2]:
                print(x)
            useranswer = input("Answer: ")

            sendData = "c " + number + " " + useranswer

            length = len(info[2])
            charLength = chr(ord('`')+length)
            stop = 0

            if(useranswer <= charLength and useranswer != ""):
                sendData = json.dumps(sendData)
                s.send(sendData.encode())
                rcvdData = s.recv(1024).decode()
                response = json.loads(rcvdData)
                print(response)

            else:
                while stop == 0:
                    useranswer = input(
                        "That's not an option. Please enter your answer: ")
                    if useranswer == "":
                        continue
                    elif(useranswer <= charLength):
                        sendData = "c " + number + " " + useranswer
                        sendData = json.dumps(sendData)
                        s.send(sendData.encode())
                        rcvdData = s.recv(1024).decode()
                        response = json.loads(rcvdData)
                        print(response)
                        break

    elif qtypefirst == 'c':
        qtyperest = qtyperest.replace(" ", "")
        qnumber = qtyperest[:-1]
        qtrialanswer = qtyperest[-1]
        qtype = "c " + qnumber + " " + qtrialanswer
        sendData = json.dumps(qtype)
        s.send(sendData.encode())
        rcvdData = s.recv(1024).decode()
        response = json.loads(rcvdData)

        print(response)
    elif(qtypefirst == 'k'):
        print("Ending server")
        sendData = "End server"
        sendData = json.dumps(sendData)
        s.send(sendData.encode())

    elif(qtypefirst == 'q'):
        print("Ending client")
        sendData = "Ending client"
        sendData = json.dumps(sendData)
        s.send(sendData.encode())
        break

    elif qtypefirst == 'h':
        helpinfo = "Options: \n\np: put question in the question bank. Each section is separated with a period on a blank line. Enter tags, question text, choices separated by a period each and then an additional period after all choices have been entered and the correct answer. \n\nd: delete a question from the bank. Enter d followed by the number you wish to delete. \n\nr: get a random question from the bank. It will display the question and list of option. Select the answer you think it is and then hit enter. \n\nc: check answer to a question. Enter c followed by the question number you want to check and then the answer you wish to check in the format c <question number> <answer>. It will return correct or incorrect. \n\nq: terminate the client\n\nk: terminate the server\n\nh: print these instructions"
        print(helpinfo)

    elif qtypefirst == 's':
        # set contest
        sendData = json.dumps(qtype)
        s.send(sendData.encode())
        rcvdData = s.recv(1024).decode()
        response = json.loads(rcvdData)
        if response[0:5] == "Error":
            print(response)
        else:
            print("number cleared for the taking")
            f = open("contest" + response + ".txt", "w+")

    else:
        print("Command not recognized")


s.close()
