# ⚠ This Server does not need to be run! ⚠
It is already deployed on Heroku, and the TicTacToe Project is already set up to use that URL.

# Flask REST API
This Server manages the backend of my TicTacToe AI, storing the game data inside a PostgresSQL database.

# Contents
- [⚠ This Server does not need to be run! ⚠](#-this-server-does-not-need-to-be-run-)
- [Flask REST API](#flask-rest-api)
- [Contents](#contents)
- [Installing dependencies](#installing-dependencies)
- [Setting up Environment Variables](#setting-up-environment-variables)
    - [Note](#note)
- [Creating the Tables](#creating-the-tables)
- [Running the Server](#running-the-server)
- [Routes](#routes)
  - [GET /score](#get-score)
  - [POST /score](#post-score)
- [Rate Limiting](#rate-limiting)

# Installing dependencies
For development, it is preferred to use `pipenv` to install dependencies.

```properties
pipenv shell
pipenv install
```

Heroku doesn't use `pipenv`, so a `requirements.txt` file needs to be generated with the following command:
```properties
pipenv lock -r > requirements.txt
```

If you do not use `pipenv` either, you may install the dependencies directly from `requirements.txt` with `pip`.
```properties
pip install requirements.txt
```

# Setting up Environment Variables

These `.env` variables will be loaded and used to configure the server. 
This is useful to hide any criticial information, or vary variables across development, testing, and production enviroments. 
For this reason, avoid committing `.env` variables, ignore them by adding them to [.gitignore](./.gitignore)!

Copy [.env.example](./.env.example) **and rename the copy** to `.env`.
Put your PostgreSQL or SQLite URI inside and rename the file to `.env`.

- `DATABASE_URL` should be your database's URI.
- `FLASK_ENV` should be set to `development` if you want to see debug information.

The `dotenv` library will then handle loading in the `.env` file. Alternatively, `pipenv` automatically loads `.env` files.

```py
import dotenv
dotenv.load_dotenv()
```

Afterwards, you can access those variables through the `os` library.
```py
import os
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Note
If you don't want to setup a PostgreSQL instance locally, you can use [SQLite](https://www.sqlite.org/about.html) instead.
All you need to do is set the `DATABASE_URL` to `"sqlite+pysqlite:///tictactoe.db"`, and a database of the name `tictactoe.db` will be created automatically.
However, [Heroku doesn't support SQLite](https://devcenter.heroku.com/articles/sqlite3), and you will need to use [another database for production](https://www.heroku.com/postgres).

# Creating the Tables
To create the required tables, run `pipenv create_db.py`.

```properties
pipenv create_db.py
```

# Running the Server
To run the server in development mode:
```properties
pipenv run python app.py
```

Python is single threaded, and won't be able to handle much load on it's own in production. 
[guinicorn](https://gunicorn.org/) is used to scale the server, and restart it if it crashes.

To run the server in production mode:
```properties
pipenv run gunicorn app:app
```

Finally, if you want the [Frontend GUI](https://github.com/RyanSamman/TicTacToeAI) to use your server, go to `/TicTacToe/util.py` and change `SERVER_URL` to the Flask Server's URL, which will be `http://127.0.0.1:5000` by default. If you want to deploy the server onto Heroku, [follow this tutorial.](https://devcenter.heroku.com/articles/getting-started-with-python)

# Routes

## GET /score
[Retrieves a JSON response](https://ryans-ttt.herokuapp.com/score) of all the games stored on the database.

Returns the JSON data and a 200 response code if successful.

## POST /score
Adds a game to the database.

Returns the new game added and a 201 response code if successful.
Otherwise, will return some text along with a 400 response code.

# Rate Limiting

To mitigate DDoS attacks, the routes are `rate limited`
```py
from flask import Flask
from flask_limiter import Limiter

app = Flask(__name__)
Limiter(app, key_func=get_remote_address, default_limits=["500 per day", "60 per hour"])
```
