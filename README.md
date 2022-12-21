
# Todo Website

Todo website stores the todo list of a user. User can view his/her todos, create a new todo, update an existing todo and delete todo.


## Tech Stack

**Client:** HTML, CSS, JavaScript, Bootstrap 5

**Server:** Python, flask, Firebase, Pyrebase

  
## Run Locally

Clone the project

```bash
  git clone https://github.com/askandola/todo_website.git
```

Go to the project directory

```bash
  cd todo_website
```

If you want use virtual environment

```bash
  virtualenv venv
```

```bash
  venv/Scripts/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Make a Firebase project for a web app. Set up authentication(enable for Email/Password) and realtime database. Then add Firebase configuration object containing keys and identifiers to 'firebaseConfig' variable in 'app.py' file.

Start the server

```bash
  python ./app.py
```

  
