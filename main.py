import time, sqlite3
from glob import glob
from settings import *; clear()
from database_api import Api

# ############################ #

class Files:
    def __init__(self, folder, mask):
        self.__folder = folder
        self.__mask = mask

    @property
    def folder(self):
        return self.__folder
      
    @property
    def mask(self):
        return self.__mask

    def active_files(self, dbg=False) -> list: 
        target = []
        path = self.folder
        os_path = os.path.join

        for file_name in glob(os_path(path, self.mask)):
            with open(os_path(os.getcwd(), file_name), 'r'):
                target.append(file_name)
                
        if dbg: 
            print(f"Available files:\n{target}\n")

        return target

    def log_parser(self, cur_file) -> list:
        res = []        
        with open(cur_file, "r") as f:
            for e in parser.parse_lines(f):
                res.append(parser.parse(e.entry))

        return res

class Database:
    def __init__(self, db):
        self.__db = db
        if not help and not api_mode:
            print(f"Connecting to '{db}'.")
        self.__con = sqlite3.connect(db, check_same_thread = False)
        self.__cur = self.connection.cursor()
        try: time.sleep(1)
        except: ...
        if not help and not api_mode:
            print(f"Successfuly connected.")
        try: time.sleep(0.5)
        except: ...

        clear()

        try: # create table on startup
            with open("create_table.sql") as f:
                self.cursor.execute(f.readline())
            print(f"Setting up '{db}'.\n")
        except Exception as e: 
            next
        try:
            self.cursor.execute("SELECT count(*) FROM Logs")
            self.__rows = self.cursor.fetchone()[0]
            self.updated = 0
        except Exception as e:
            print(e)
        

    def __repr__(self): 
        return self.__db
    
    @property
    def rows(self):
        return self.__rows
    
    @rows.setter
    def rows(self, value):
        self.__rows = value
    
    @property
    def connection(self): 
        return self.__con

    @property
    def cursor(self): 
        return self.__cur
    
    def truncate(self): 
        try:
            self.cursor.execute("DELETE FROM Logs")
            self.connection.commit()
            self.rows = 0
        except Exception as e: 
            next
    
    def query(self, req, dbg=False):
        try:
            self.cursor.execute(req)
            self.connection.commit()
            if dbg:
                fetch = self.cursor.fetchall()
                for i in range(len(fetch)):
                    print(f"{fetch[i]}\n"[:-1]) # ~ str.strip()
        except Exception:
            next

    def apply_filters(self, api=None) -> list:
        prompt = api or user_input(prompt_msg)
        list_of_fields = str_trim(prompt)

        fields = ""
        if prompt:
            for key in list_of_fields: 
                try:
                    fields += fields_dict[key] + ","
                except Exception:
                    next

        return prompt != '', fields[:-1], list_of_fields
    
    def viewer(self, sort_type="ASC"):
        col = "remote_host"
        apply = self.apply_filters()
        prompt = apply[0]
        fields = apply[1]
        what = prompt and fields or '*'

        que = f"SELECT {what} FROM Logs ORDER BY"
        req = f'{que} {col} {sort_type}'

        print(f"\nFiltered data: ")
        self.query(req, True)
        print()

    def sort_by(self, arg1=None, sort_type="ASC"):
        if not arg1: return 

        sort_type = sort_type.upper()
        vari = ["DATE", "DATETIME", "TIMESTAMP"]
        col = "remote_host"
        apply = self.apply_filters()
        prompt = apply[0]
        fields = apply[1]

        que = f"SELECT {prompt and fields or '*'} FROM Logs ORDER BY"
        
        if arg1.upper() in vari:
            col = "request_time"
            req = f'{que} {col} {sort_type}'
        else:
            req = f'{que} {col} {sort_type}'

        print(f"\nSorting by {col}:", sort_type)
        self.query(req, True)
        print()
    
    def group_by_ip(self, arg1=None, arg2=None):
        if not arg1: return 

        col = "remote_host"
        apply = self.apply_filters()
        prompt = apply[0]
        fields = apply[1]

        que = f"SELECT {prompt and fields or '*'} FROM Logs WHERE"

        if arg2: 
            req = f'{que} {col} = "{arg1}" AND final_status = {arg2}'
        else:
            req = f'{que} {col} = "{arg1}"'

        print(f"\nGrouping by '{arg1}':", arg2)
        self.query(f'{req} ORDER BY {col} ASC', True)
        print()

    def group_by_date(self, arg1=None, arg2=None):
        if not arg1: return 
        col = "request_time"
        apply = self.apply_filters()
        prompt = apply[0]
        fields = apply[1]

        que = f"SELECT {prompt and fields or '*'} FROM Logs WHERE"

        if arg2: 
            req = f'{que} {col} BETWEEN "{arg1}" AND "{arg2}" GROUP BY {col}'
        else:
            if len(arg1) == 10:
                req = f'{que} {col} BETWEEN "{arg1} 00:00:00+00:00" AND "{arg1} 23:59:59+00:00" GROUP BY {col}'
            else:
                req = f'{que} {col} = "{arg1}+00:00" GROUP BY {col}'

        print(f"\nGrouping by {arg1}{arg2 and ', ' or ''}{arg2}:")
        self.query(f'{req} ORDER BY {col} ASC', True)
        print()

# ########################### #

if not batch_mode and not interactive and not help:
    help = True

database = Database(db_name)

if api_mode:
    api = Api(database)
    ln = len(argv)

    try: switch = int(api_function)
    except Exception: quit()

    match switch:
        # @api_viewer(fields)
        case 1: 
            apply = ln > 3 and argv[3][1:-1] or "-"
            req_filter = apply.split(",")
            logs = api.viewer(apply)
            try: 
                output = create_json(apply, logs, req_filter)
                print_json(output)
            except Exception: 
                json_err()

        # @api_sort_by(sort_column, fields, asc|desc)
        case 2:
            if ln <= 3: 
                json_err()
            
            sort_type = argv[3]
            apply = ln > 4 and argv[4][1:-1] or "-"
            req_filter = apply.split(",")
            order = ln > 5 and argv[5] or "asc"
            logs = api.sort_by(sort_type, apply, order)
            try: 
                output = create_json(apply, logs, req_filter)
                print_json(output)
            except Exception: json_err()

        # @api_group_by_ip(exact_ip, status, fields)
        case 3: 
            if ln < 4: 
                json_err()

            if ln <= 4:
                status = None
            else:
                status = argv[4][0] == "[" and None or argv[4]

            exact_ip = argv[3]
            apply = (ln > 4 and argv[-1][0] == "[") and argv[-1][1:-1] or "-"
            req_filter = apply.split(",")

            logs = api.group_by_ip(exact_ip, status, apply)
            try: 
                output = create_json(apply, logs, req_filter)
                print_json(output)
            except Exception: json_err()

        # @api_group_by_date(exact_date, second_date, fields)
        case 4: 
            if ln < 4: 
                json_err()

            exact_date = argv[3]
            
            if ln <= 4:
                arg2 = None
            else:
                arg2 = argv[4][0] == "[" and None or argv[4]

            apply = (ln > 4 and argv[-1][0] == "[") and argv[-1][1:-1] or "-"
            req_filter = apply.split(",")
            logs = api.group_by_date(exact_date, arg2, apply)
            try: 
                output = create_json(apply, logs, req_filter)
                print_json(output)
            except Exception: json_err()
        case _:
            print("Incorrect parameters. See documentation. \n")
            quit()
    
welcome()
state()

if help: 
    helper()
    redirect = user_input("To continue, you can enter -i or -b: ")
    batch_mode = redirect == "-b"
    interactive = redirect == "-i"
    api_mode = redirect == "-a"

    if api_mode: 
        print("Apache Log Viewer API:\n\nShould be accessed with command line argument!")

    if batch_mode or interactive:
        help = False; print(); 

files = Files(active_folder, file_mask)

def update_logs(db, to):
    db.updated = 0

    for f in to:
        data = files.log_parser(type(to) is list and f or to)
        for v in data:
            di = vars(v)
            try:
                req = f"INSERT INTO Logs(remote_host, remote_logname, remote_user, request_line, final_status, bytes_sent, request_time)VALUES ('{di['remote_host']}', '{di['remote_logname']}', '{di['remote_user']}', '{di['request_line']}', {di['final_status']}, {di['bytes_sent']}, '{di['request_time']}')"
                db.query(req)
            except Exception as e:
                next

    db.cursor.execute("SELECT count(*) FROM Logs")
    count = db.cursor.fetchone()[0]

    db.updated = abs(db.rows-count)
    db.rows = count
    color = '\033[0;92m'
    white = '\033[0m'

    print(f'Active folder: {color}"{active_folder}"\n{white}File mask: {color}"{file_mask}"\n{white}')
    try:
        init(database, True)
    except Exception as e:
        print(e)

if batch_mode:
    update_logs(database, files.active_files(True))

if interactive:
    try:
        init(database)
    except Exception as e:
        print(e)

    while repeat:
        menu()
        choice = user_input("Enter a number of function: ", int); print()
        if choice == "q": sys_exit(0)
        match choice:
            case 1:
                database.viewer()
                p = user_input("[?] Continue: "); print()
                if p.lower() not in answers: repeat = False
            case 2:
                p = user_input("Sort by: [IP/DATE] [ASC/DESC] \n> "); print()
                arg = str_trim(p)
                arg2 = len(arg) > 1 and arg[1] or "asc"
                database.sort_by(arg[0], arg2)
                p = user_input("[?] Continue: "); print()
                if p.lower() not in answers: repeat = False
            case 3:
                p = user_input("Group by: [IP/IP + Status] \n* Make sure to enter exact IP or IP with status!\n> "); print()
                arg = str_trim(p)
                arg2 = len(arg) > 1 and arg[1] or None
                database.group_by_ip(arg[0], arg2)
                p = user_input("[?] Continue: "); print()
                if p.lower() not in answers: repeat = False
            case 4:
                p = user_input("Group by: [Date/Period] \n* Make sure to enter exact date or period!\n> "); print()
                arg = str_trim(p)
                arg2 = len(arg) > 1 and arg[1] or ""
                database.group_by_date(arg[0], arg2)
                p = user_input("[?] Continue: "); print()
                if p.lower() not in answers: repeat = False
            case 5:
                print("Clearing logs...")
                database.truncate()
                try: time.sleep(1)
                except: ...
                print()
            case 6:
                update_logs(database, files.active_files(True))
            case _:
                print("This function doesn't exist yet.\n")

    goodbye() 
    any_key()
