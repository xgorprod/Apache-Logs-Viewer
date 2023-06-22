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
python main.py -a 1 filters: [, ...]
```
e.g:
``` Python
python main.py -a 1 [ip,status,date]
```
