# Core Twitch bot, with all the functions

import socket
# import time
import configparser
import re
import msvcrt
# import random
from core.commands import *

# Object Session for handle multiple connections if you want


class Session (object):
    def __init__(self, host, port, nick, passwd, chan):
        self.host = host
        self.port = port
        self.nick = nick
        self.passwd = passwd
        self.chan = chan
        self.loading = True
        self.spamcount = 0
        self.chatmsg = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
        self.s = socket.socket()
        self.connection()

    def connection(self):
        self.s.connect((self.host, int(self.port)))
        self.s.send("PASS {}\r\n".format(self.passwd).encode("utf-8"))
        self.s.send("NICK {}\r\n".format(self.nick).encode("utf-8"))
        self.s.send("JOIN {}\r\n".format(self.chan).encode("utf-8"))

    # Function to join a room
    def joinroom(self):
        readbuffer = ''
        while self.loading:
            readbuffer = readbuffer + self.s.recv(1024).decode("utf-8")
            temp = readbuffer.split("\n")
            temp.pop()
            readbuffer = temp.pop()
            temp = readbuffer.split(':')
            if "End of /NAMES list\r" == temp[2]:
                self.loading = False
        #message = 'forsenLewd'
        #self.sendmessage(message)

    # Respon the commands
    def initbot(self):
        while True:
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 27:
                    break
            else:
                try:
                    response = self.s.recv(1024).decode("utf-8")
                    if response == "PING :tmi.twitch.tv\r\n":
                        self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                    else:
                        username = re.search(r"\w+", response).group(0)  # return the entire match
                        message = self.chatmsg.sub("", response)
                        order = controller(username, message)
                        if order != '':
                            self.sendmessage(order)
                        print(username + ": " + message)
                except UnicodeDecodeError:
                    pass
                except AttributeError:
                    pass
            #time.sleep(0.1)

    # Only reads chat
    def readchat(self):
        while True:
            if msvcrt.kbhit():
                if ord(msvcrt.getch()) == 27:
                    break
            else:
                try:
                    response = self.s.recv(1024).decode("utf-8")
                except UnicodeDecodeError:
                    pass
                except AttributeError:
                    pass
                if response == "PING :tmi.twitch.tv\r\n":
                    self.s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                username = re.search(r"\w+", response).group(0)  # return the entire match
                message = self.chatmsg.sub("", response)
                print(username + ": " + message)
            time.sleep(0.1)

    def sendmessage(self, message, point):
        if point:
            messagetemp = "PRIVMSG " + self.chan + " :" + message + ' .' + '\r\n'
            point = False
        else:
            messagetemp = "PRIVMSG " + self.chan + " :" + message + '\r\n'
            point = True
        self.s.send(messagetemp.encode("utf-8"))
        return point

    # Spam mode, Time and Message as a input.
    def spammode(self, spam, spam_t):
        point = True
        while True:
            try:
                if msvcrt.kbhit():
                    if ord(msvcrt.getch()) == 27:
                        break
                else:
                    point = self.sendmessage(spam, point)
                    self.spamcount += 1
                    print('You sent ' + str(self.spamcount) + ' spam messages')
                    time.sleep(int(spam_t))

            except ConnectionResetError:
                self.s = socket.socket()
                self.connection()
                self.joinroom()
                self.spammode(spam, spam_t)

    def rk9(self, spam, spam_t):
        point = True
        while True:
            try:
                if msvcrt.kbhit():
                    if ord(msvcrt.getch()) == 27:
                        break
                else:
                    spamrk9 = str(random.randint(0, 10000)) + " " + spam
                    point = self.sendmessage(spamrk9, point)
                    self.spamcount += 1
                    print('You sent ' + str(self.spamcount) + ' spam messages')
                    time.sleep(int(spam_t))

            except ConnectionResetError:
                self.s = socket.socket()
                self.connection()
                self.joinroom()
                self.rk9(spam, spam_t)


def openconf():
    # Open config file, and read all the variables, you can choose the channel if you type nothing, you get the default.
    config = configparser.ConfigParser()
    config.read('config.cfg')
    host = config['CONFIG']['HOST']  # the Twitch IRC server
    port = config['CONFIG']['PORT']  # always use port 6667!
    nick = config['CONFIG']['NICK']  # your Twitch username, lowercase
    passwd = config['CONFIG']['PASS']  # your Twitch OAuth token
    chan = config['CONFIG']['CHAN']  # the channel you want to join
    session = Session(host, port, nick, passwd, chan)
    return session


def defaultmenu():
    ascii_menu()
    print('Choose your option')
    print('1) Init the bot ')
    print('2) Read the Chat Only ')
    print('3) Template SPAM Mode ')
    print('4) SPAM Mode ')
    print('5) R9K Mode ')
    print('6) Exit ')


def ascii_menu():
    print('''
  _____ __      __ ___  _____  ___  _  _   ___   ___  _____
 |_   _|\ \    / /|_ _||_   _|/ __|| || | | _ ) / _ \|_   _|
   | |   \ \/\/ /  | |   | | | (__ | __ | | _ \| (_) | | |
   |_|    \_/\_/  |___|  |_|  \___||_||_| |___/ \___/  |_|
    ''')
