import requests
import sys
import json
import os
from base64 import b64encode, b64decode
import json
import time


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


CONFIG_FILE = os.path.join(os.path.expanduser('~'), '.cli_chat_config')

def get_headers():
        try:
                with open(CONFIG_FILE) as f:
                        return json.loads(f.read())
        except IOError:
                print("No user configs found")
                return {}
        
HEADERS = get_headers() #TURN THIS INTO A CLASS

def set_header(param_str):
        header, val = param_str.split(' ', 1)
        HEADERS[header] = val
        with open(CONFIG_FILE, 'w') as f:
                f.write(json.dumps(HEADERS))

def switch_room(new_room):
        global ROOM
        ROOM = new_room

def enter_read_mode(_):
        global MODE
        MODE = 'read'

CMDS = {
        '\\set': set_header,
        '\\room': switch_room,
        '\\read': enter_read_mode
        }
def parse_msg(msg):
        if ' ' in msg:
                cmd, arg = msg.split(' ', 1)
        else:
                cmd, arg = (msg, '')
        if cmd in CMDS:
                CMDS[cmd](arg)
        else:
                msg = b64encode(msg)
                payload = HEADERS.copy()
                payload['msg'] = msg.decode('utf-8')
                requests.post("http://waksmemes.x10host.com/mess/?" + ROOM + '!post',
                                json = payload)

def parse_shell_args():
        mode = 'chat'
        room = "linusXD2"
        for arg in sys.argv[1:]:
                if arg[0] == '-':
                        if arg == '-r':
                                mode = 'read'
                else:
                        room = arg
        return room, mode

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
                name = d.get('name', d['ip'])
                name_color = d.get('color', DEFAULT_NAME_COLOR)
                msg = b64decode(d.get('msg', '')).decode('utf-8')
                print(color(name + ': ', name_color) + color(msg, TEXT_COLOR))
        return last_id

def clear_screen():
        os.system('cls') if sys.platform[:3] == 'win' else os.system('clear')


ROOM, MODE = parse_shell_args()
LAST_ID = 0
clear_screen()
while 1:
        if MODE == 'chat':
                fetch_and_print(True)
                new_msg = raw_input('> ')
                if new_msg != '':
                        parse_msg(new_msg)
        else:
                LAST_ID = fetch_and_print(False, LAST_ID)
                time.sleep(0.5)
