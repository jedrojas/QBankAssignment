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


s.close()
