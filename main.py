#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Twitch chat mini spam bot v 0.2

from core.core import *
from core.commands import templatelist, gettext

import random

connection = openconf()
connection.joinroom()

while True:
    defaultmenu()
    menu = input('Choose your option: ')
    if menu == '1':
        connection.initbot()
    elif menu == '2':
        connection.readchat()
    elif menu == '3':
        template = templatelist()
        position = 1
        for i in template:
            print(str(position) + ") " + i)
            position += 1
        number = input('Number: ')
        spam = gettext(template[int(number)-1])
        time = input('Introduce the time: ')
        spam = '/me ' + spam
        connection.spammode(spam, time)
    elif menu == '4':
        spam = input('Introduce the spam: ')
        time = input('Introduce the time: ')
        spam = '/me ' + spam
        connection.spammode(spam, time)
    elif menu == '5':
        spam = input('Introduce the spam: ')
        time = input('Introduce the time: ')
        connection.rk9(spam, time)
    elif menu == '6':
        break
    else:
        print('Wrong!')