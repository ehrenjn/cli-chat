#!/usr/bin/python3

import requests
import sys
import json
import os
from base64 import b64encode, b64decode
import json
import time
import datetime
import pytz

#Colors======================================
COLORS = {
        'red': "\x1b[1;31m",
        'green': "\x1b[1;32m",
        'yellow': "\x1b[1;33m",
        'blue': "\x1b[1;34m",
        'purple': "\x1b[1;35m",
        'cyan': "\x1b[1;36m"
        }
STOP_COLOR = "\x1b[0m"
DEFAULT_NAME_COLOR = STOP_COLOR
TEXT_COLOR = "\x1b[3;2m"
def color(string, color_string):
        if color_string[0] != '\x1b':
                color_string = COLORS.get(color_string, STOP_COLOR)
        return color_string + string + STOP_COLOR

#User Settings===============================
CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.cli_chat_config')

def get_settings():
        try:
                with open(CONFIG_FILE) as f:
                        return json.loads(f.read())
        except IOError:
                print("No user configs found")
                return {}
        
SETTINGS = get_settings() #TURN THIS INTO A CLASS

def set_setting(param_str):
        setting, val = param_str.split(' ', 1)
        SETTINGS[setting] = val
        with open(CONFIG_FILE, 'w') as f:
                f.write(json.dumps(SETTINGS))

#Commands====================================
def switch_room(new_room):
        global ROOM
        ROOM = new_room

def enter_read_mode(_):
        global MODE
        MODE = 'read'

def flush_pipes(_):
	flush_depth = 300
	for a in range(flush_depth):
		parse_msg("flushing the pipes: " + str(flush_depth - a))
	parse_msg("the pipes are clean!")

CMDS = {
        '\\set': set_setting,
        '\\room': switch_room,
        '\\read': enter_read_mode,
	'\\flush': flush_pipes
        }

#Parsing==============================
def parse_msg(msg):
        if ' ' in msg:
                cmd, arg = msg.split(' ', 1)
        else:
                cmd, arg = (msg, '')
        if cmd in CMDS:
                CMDS[cmd](arg)
        else:
                msg = b64encode(bytes(msg, encoding = 'UTF-8'))
                settings = b64encode(bytes(json.dumps(SETTINGS), encoding = 'UTF-8'))
                payload = {
                        'msg': msg.decode('utf-8'),
                        'settings': settings.decode('utf-8')
                        }
                requests.post("http://waksmemes.x10host.com/mess/?" + ROOM + '!post',
                                json = payload)
'''
#might come in handy later, not sure if it's needed yet
def errorless_print(string):
    try:
        print(string)
    except UnicodeEncodeError:
        try: #try to print 0th plane chars
            print(''.join(s for s in string if ord(s) < 65536))
        except UnicodeEncodeError: #if that's broken just print ascii chars
            print(string.encode('ascii', errors = 'ignore').decode('ascii'))
'''

def parse_shell_args():
        mode = 'chat'
        room = "main"
        for arg in sys.argv[1:]:
                if arg[0] == '-':
                        if arg == '-r':
                                mode = 'read'
                else:
                        room = arg
        return room, mode

#Platform independance=======================
def clear_screen():
        os.system('cls') if sys.platform[:3] == 'win' else os.system('clear')

if sys.version_info[0] < 3:
        bytes = lambda s, encoding: s.encode('utf-8') #so that you can't send malformed unicode
        input = raw_input


#Main========================================
def fetch_and_print(clear, ids_after = 0, max_msgs = 100):
        res = requests.post("http://waksmemes.x10host.com/mess/?" + ROOM,
                           json = {'MAX_MSGS': max_msgs, 'id': {'min': ids_after + 1}})
        raw = res.content.decode('utf-8')
        data = json.loads(raw)
        data.reverse()
        if clear:
                clear_screen()
        last_id = ids_after
        for d in data:
                last_id = d['id']
                timestamp = d['time']
                timestr = '[' + datetime.datetime.fromtimestamp(timestamp, 
                        tz = pytz.timezone('US/Eastern')).strftime("%H:%M:%S") + '] '
                settings = {}
                if 'settings' in d:
                    raw_settings = b64decode(d['settings']).decode('utf-8')
                    settings = json.loads(raw_settings)
                name = settings.get('name', d['ip'])
                name_color = settings.get('color', DEFAULT_NAME_COLOR)
                msg = b64decode(d.get('msg', '')).decode('utf-8')
                print(timestr + color(name + ': ', name_color) + color(msg, TEXT_COLOR))
        return last_id


ROOM, MODE = parse_shell_args()
LAST_ID = 0
clear_screen()
while 1:
        if MODE == 'chat':
                fetch_and_print(True)
                new_msg = input('> ')
                if new_msg != '':
                        parse_msg(new_msg)
        else:
                LAST_ID = fetch_and_print(False, LAST_ID)
                time.sleep(0.5)

#IF EVERYTHING BREAKS: HEAD ON OVER TO THE disaster ROOM