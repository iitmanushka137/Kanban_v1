# Local Setup
- Run ```pip install -r requirements.txt``` to install all dependencies written in ```requirements.txt``` which is inside ```docs``` folder

# Local Development Run
- ```python3 app.py``` It will start the flask app in ```development```. This is for running app on local system.

# Replit Run
- Add the ```requirements.txt``` in ```poetry```
- Go to the shell and run ```pip install --upgrade poetry```
- Select and open the ```main.py``` python file and click on Run button
- The web app will be available at https://Project.iitmanushka137.repl.co
- Format will be sort of https://..repl.co

# Folder Structure
- ```project.sqlite3``` is the sqlite database. It can be anywhere on the machine, just the adjustment in the path in ```app.py``` is required. One of the database is shipped for testing.
- The application code for my app is ```/```
- ```static``` a folder in which we have ```IMG``` folder which has images used in the app. Also the graphs generated are saved in it.
- ```templates``` is the default folder where templates are stored
```
Project/
├── app.py
├── models.py
├── project.sqlite3
├── readme.md
├── Project Documentation.pdf
├── docs
|   └── requirements.txt
├── static/
│   └── IMG/
|       ├── 1.png
|       ├── 2.png
|       ├── 3.png
|       └── add.png
├── templates/
│   ├── card_adding.html
│   ├── cardname_error.html
│   ├── complete_incomplete.html
│   ├── delete_card_permission.html
│   ├── delete_list_permission.html
│   ├── listname_error.html
│   ├── list_adding.html
│   ├── login_page.html
|   ├── Summary.html
|   ├── update_list.html
|   ├── updated_home_page.html
|   └── username_error.html
└──
```