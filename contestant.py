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
questionDict = {}

rcvdData = s.recv(1024).decode()
response = json.loads(rcvdData)
print(response)
# just printed out contest joined

rcvdData = s.recv(1024).decode()
question = json.loads(rcvdData)
print(question)
# just asked for nickname

nickname = input()
sendData = json.dumps(nickname)
s.send(sendData.encode())
# just sent nickname

nicknametaken = True
while nicknametaken:
    rcvdData = s.recv(1024).decode()
    response = json.loads(rcvdData)
    print(response)
    if response[0:5] == "Error":
        nickname = input()
        sendData = json.dumps(nickname)
        s.send(sendData.encode())
    else:
        nicknametaken = False
# nickname in, time to start answering questions

quizinprogress = True
while quizinprogress:
    rcvdData = s.recv(1024).decode()
    question = json.loads(rcvdData)
    if question[0:5] == "Break":
        print("The contest is over - thanks for playing " + nickname + "!")
        break
    else:
        print(question)

    answer = input("Enter your choice:")
    answer = json.dumps(answer)
    s.send(answer.encode())
    # just sent answer, waiting to see if right or wrong

    rcvdData = s.recv(1024).decode()
    reply = json.loads(rcvdData)
    # got a name request

    sendData = json.dumps(nickname)
    s.send(sendData.encode())
    # sent name

    rcvdData = s.recv(1024).decode()
    reply = json.loads(rcvdData)
    print(reply)
    # just got correct/incorrect and my stats

    # getting more stats
    rcvdData = s.recv(1024).decode()
    res = json.loads(rcvdData)
    print(res)


s.close()
