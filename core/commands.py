# All the commands for the bot here.
import redis
import random
import time


def controller(username, message):

    splitmessage = message.split(' ')
    response = ''
    timeout = 3

    r = redis.StrictRedis(
        host='192.168.1.3',
        port=6379,
        db=0
    )

    try:
        if username == 'twitchnotify':
            response = newfag(splitmessage[0])
        elif message[:-2] == '!weeb':
            response = "/me You're " + str(random.randint(0, 101)) + "% weeb " + username + " nyanPls nyanPls nyanPls"
            time.sleep(timeout)
        elif message[:-2] == '!trihard' or message[:-2] == '!black':
            response = "/me You're " + str(random.randint(0, 101)) + "% trihard " + username + " TriHard Clap"
            time.sleep(timeout)
        elif message[:-2] == '!iq':
            response = "/me " + username + " your IQ is " + str(random.randint(40, 210)) + " forsenIQ Clap"
            time.sleep(timeout)
        elif message[:-2] == '!??':
            response = r.get('??').decode("utf-8")
            time.sleep(timeout)
        else:
            try:
                response = '/me ' + r.get(message[1:-2]).decode("utf-8")
            except AttributeError:
                pass
    except IndexError:
        pass

    return response


def newfag(username):
    message = '/me Welcome to the team ' + username + ' forsenPuke forsenPuke3 forsenPuke4 ' \
                                                                                'forsenLewd gachiBASS Clap '
    return message


def templatelist():
    template = []
    r = redis.StrictRedis(
        host='192.168.1.3',
        port=6379,
        db=2
    )
    for key in r.keys():
        template.append(key.decode('utf-8'))
    return template


def gettext(key):
    r = redis.StrictRedis(
        host='192.168.1.3',
        port=6379,
        db=2
    )
    text = r.get(key).decode("utf-8")
    return text
