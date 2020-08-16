# ⚠ This Server does not need to be run! ⚠
It is already deployed on Heroku, and the TicTacToe Project is already set up to use that URL.

# Flask REST API
This Server manages the backend of my TicTacToe AI Analytics, storing the data inside a PostgresSQL database.

# Running the Server
## Install dependencies
```
pip install requirements.txt
```

or, more preferably

```
pipenv shell
pipenv install
```

## Setting up Environment Variables
Inside `.env.example`, Put your PostgresSQL or SQLite URI inside and rename the file to `.env`

## Creating the Database
To create the databases, run `pipenv create_db.py`

## Running the server
To run the server in development mode, run `pipenv app.py`

For production mode, run `pipenv run gunicorn app:app`

Finally, if you want the Frontend GUI to use your server, go to `/TicTacToe/util.py` and change `SERVER_URL` to the Flask Server's URL, which will be `http://127.0.0.1:5000` by default

## Deploying to Heroku
### WIP