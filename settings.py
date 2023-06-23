import msvcrt
import sys, os, time
from apachelogs import LogParser
from rich.progress import track

# Setup region
db_name = "db/database.sqlite"
active_folder = "apache"
file_mask = "*.log"

# Functions region
def sys_exit(delay=1):
    try: time.sleep(delay)
    except: ...
    sys.exit()

def user_input(msg=None, f=str):
    try:
        raw = input(msg)
        try:
            p = f(raw)
            return p
        except ValueError:
            print(f"Value Error: Must be '{f.__name__}'")
    except KeyboardInterrupt:
        print('\nKeyboard Interrupt.')
        quit()
    except EOFError:
        print('\nSee ya! ⋖|︶。︶|⋗')
        quit()
    except Exception as e:
        print(e)
        quit()

def init(db, on_upd=False):
    n = db.rows or 1
    speed = n < 3000 and n/(n*n) or (n/(n*n))/n 

    text = on_upd and (db.updated > 0 and "Updating database: " or "Loading database: ") or "Reading database: "
    for _ in track(range(n), description=text): 
        try: time.sleep(speed) 
        except: ...

    try: time.sleep(.25) 
    except: ...

    if on_upd: 
        print(f"> Found {db.rows} records.")
        print(f"> Updated rows: {db.updated}\n")
    else:
        print(f"> Found {db.rows} records.\n")

def state(): 
    msg = None
    if batch_mode or str(redirect) == '-b': msg = "Batch mode"
    if interactive or str(redirect) == '-i': msg = "Interactive mode"
    if msg: print(f'\n# Currently in {msg}.\n')

def any_key(): # checks input chars w/o pressing enter
    if msvcrt.getch():
        quit()

def str_trim(string):
    res = []
    sp = string.split
    for i in "," in string and sp(",") or sp(" "): res.append(i.strip())
    return res

def print_json(arr):
    print("{")
    for el in arr: print(f'   {el},')
    print("}")
    quit()
    
def json_err(): 
    print("{\n}")
    quit()

def create_json(switch, data, req_filter):
    res = []
    for line in data:
        if switch.rstrip() == "-":
            res.append ({
                "ip" : line[1],
                "name" : line[2],
                "user" : line[3],
                "line" : line[4],
                "status" : line[5],
                "bytes" : line[6],
                "date" : line[7],
            })
        else:
            concat = ""
            for i, _ in enumerate(line):
                concat += f'{req_filter[i]} : {line[i]}, '
            
            res.append("{"+concat[:-2]+"}")

    return res

# Variables region
parser = LogParser("%h %l %u %t \"%r\" %>s %b")
#ex_parser = LogParser("%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"")

repeat = True
redirect = ''
answers = ['y', "yes", "+", '']
argv = sys.argv
cmd_param = len(argv) > 1 and argv[1] or '-h'

help = cmd_param == "-h"
batch_mode = cmd_param == "-b" or redirect == "-b"
interactive = cmd_param == "-i" or redirect == "-i"
api_mode = cmd_param == "-a"
api_function = (api_mode and len(argv) > 2) and argv[2] or 0

all_params = ["-i", "-h", "-b", "-a"]

if api_mode or help or cmd_param not in all_params:
    clear = lambda: ... 
else:
    clear = lambda: os.system('cls')

fields_dict = {
    "ip" : "remote_host",
    "name" : "remote_logname",
    "user" : "remote_user",
    "line" : "request_line",
    "status" : "final_status",
    "bytes" : "bytes_sent",
    "time" : "request_time",
    "date" : "request_time"
}

welcome_msg = 'Welcome to Apache Log Viewer.'
goodbye_msg = 'Thanks for using Apache Logs Viewer! <3\nPress any key to exit.'

help_msg = "\nAvailable command line arguments:\n\
-i = interactive mode\n\
-b = batch mode (cron)\n\
-a = api calls\n\
More details and examples in README.md\n"

menu_msg = 'List of available functions:\n\
1) Logs Viewer\n\
2) Sort by IP/Date\n\
3) Group by IP+Status\n\
4) Group by Date or Period\n\
5) Clear logs from DB\n\
6) Load logs to DB\n'

prompt_msg = "Fields to display: [ip, name, user, line, status, bytes, date]\n> "

def goodbye(): print(goodbye_msg)
def welcome(): print(welcome_msg)
def helper(): print(help_msg)
def menu(): print(menu_msg)