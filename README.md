# Apache-Logs-Viewer 🔎
A Python application for parsing/managing Apache logs

## ℹ️ Program modes:
`-h, -b, -i, -a`

## 💬 List of available functions:
- Logs Viewer
- Sort by IP/Date
- Group by IP+Status
- Group by Date or Period
- Clear logs from DB
- Load logs to DB

## 📝 Installation:
- Open setup.bat to import libraries.
- Open settings.py for customization
- Edit "Database name", "Active folder", "File mask"
  
## 🛠️ Examples: 
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
python main.py -a (**args)
```
## ⚙️ API Docs:
1) Logs Viewer
``` Python
viewer(filters: [, ...])

python main.py -a 1 [ip,status,bytes]
```
2) Sort by IP/Date
``` Python
sort_by(by: [ip/date] filters: [, ...] type: [asc/desc])

python main.py -a 2 ip [ip,date] desc
```
3) Group by IP+Status
``` Python
group_by_ip(ip status[optional] filters: [, ...])

python main.py -a 3 127.0.0.1 404
python main.py -a 3 127.0.0.1 [line,status,date]
```
4) Group by Dates
``` Python
group_by_date(date date2[optional] filters: [, ...])

python main.py -a 4 2023-06-02 2023-07-02
python main.py -a 4 2023-06-02 [ip,status,bytes]
```
