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
nameprompt = ''
questionDict = {}


while nameprompt != '1':

    nameprompt = input("Please input a nickname: ")

    sendData = json.dumps(nameprompt)
    s.send(sendData.encode())
    rcvdData = s.recv(1024).decode()
    response = json.loads(rcvdData)
    print(response)
    if response[0:5] != "Error":
        nameprompt = '1'

contestisnotover = True
while contestisnotover:
    rcvdData = s.recv(1024).decode()
    response = json.loads(rcvdData)
    print(response)


s.close()
