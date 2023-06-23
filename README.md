# Apache-Logs-Viewer 🔎
A Python application for parsing/storing/reading Apache access logs

## 💬 List of available functions:
- Logs Viewer
- Sort by IP/Date
- Group by IP+Status
- Group by Date or Period
- Clear logs from DB
- Load logs to DB

## 📝 Installation:
- Open `setup.bat` to import libraries.
- Open `settings.py` for customization 
  - `db_name` - filename of the database
  - `active_folder` - folder with Apache logs
  - `file_mask` - mask of files to parse

## ℹ️ Usage:
``` Python
python main.py [ -h | -b | -i | -a ] [parameters]
```

## 🛠️ Launch info: 
Application can be opened in different states: 
</br>
### Help: </br>
``` Python
python main.py -h
```
### Batch: </br>
``` Python
python main.py -b
```
### Interactive: </br>
``` Python
python main.py -i
```
### API: </br>
``` Python
python main.py -a <number of a function> <parameters>
```
## ⚙️ API Docs:

There are 4 API functions that allow to get JSON with log information and apply filters.

1) Logs Viewer

- Parameters: list of output fields: `[ip,name,user,line,status,bytes,date]` </br>
\* You should specify one or more fields in brackets, empty list = all fields.

**Example**: *return ip, status and bytes:*
``` Python
python main.py -a 1 [ip,status,bytes]
```
2) Sort by IP/Date

- Parameters: sort by: **IP** or **DATE**, list of output fields: `[ip,name,user,line,status,bytes,date]`, sort order: **ASC** or **DESC** </br>
\* You should specify one or more fields in brackets, empty list = all fields.

**Example**: *return ip, date sorted by ip descending:*
``` Python
python main.py -a 2 ip [ip,date] desc
```
3) Group by IP+Status

- Parameters: group by: **exact IP**, HTTP Status: **number**, list of output fields: `[ip,name,user,line,status,bytes,date]` </br>
\* You should specify one or more fields in brackets, empty list = all fields.

**Example**: *return logs grouped by 127.0.0.1 with status 404:*
``` Python
python main.py -a 3 127.0.0.1 404
```
**Example**: *return line, status, date grouped by 127.0.0.1 for every status:*
``` Python
python main.py -a 3 127.0.0.1 [line,status,date]
```

4) Group by Dates
- Parameters: date from: **DATE**, date to: **DATE 2** (optional), list of output fields: `[ip,name,user,line,status,bytes,date]` </br>
\* You should specify one or more fields in brackets, empty list = all fields.

**Example**: *return logs for the period from 2023-06-02 to 2023-07-02*
``` Python
python main.py -a 4 2023-06-02 2023-07-02
```
**Example**: *return ip, status, bytes for the one date 2023-06-02*
``` Python
python main.py -a 4 2023-06-02 [ip,status,bytes]
```