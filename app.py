import re
import os
import json
import dotenv
from datetime import datetime
from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# A Simple REST api Backend to store Game data
app = Flask(__name__)
Limiter(app, key_func=get_remote_address, default_limits=["500 per day", "60 per hour"])

# Load .env Variables & configure app
dotenv.load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None: raise Exception("Database URL was not defined")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Initialize SQL ORM (Object Relational Model)
class GameData(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	player1 = db.Column(db.String(15), nullable=False)
	player2 = db.Column(db.String(15), nullable=False)
	startingPlayer = db.Column(db.String(15), nullable=False)
	moves = db.Column(db.String(15), nullable=False)
	win = db.Column(db.Boolean(), nullable=False)
	winner = db.Column(db.String(15), nullable=True)
	draw = db.Column(db.Boolean(), nullable=False)

	# For Debugging:
	def __repr__(self):
		data = json.dumps({"id": self.id, 'moves': self.moves, 'win': self.win, 'draw': self.draw})
		return f"<GameData {data}>"


ma = Marshmallow(app) # Init Marshmallow (Object Serializer to convert to JSON)
class GameSchema(ma.Schema):
	class Meta:
		fields = ('player1', 'player2', 'startingPlayer', 'moves', 'win', 'winner', 'draw')

GameParser = GameSchema()
GamesParser = GameSchema(many=True)


def sanitizeData(data):
	print(data)
	return data


@app.route('/score', methods=['POST'])
def createGame():
	try:
		data = sanitizeData(request.json)
		print("New API")
		newGame = GameData(**data)
		print(f"{newGame!r}")
		db.session.add(newGame)
		db.session.commit()
		return GameParser.jsonify(newGame), 201
	except Exception as e:
		return Response(f"Invalid Request: {e}" , status=400)


@app.route('/score', methods=['GET'])
def getGames():
	allGames = GameData.query.all()
	print(f"{allGames!r}")
	return GamesParser.jsonify(allGames)


if __name__ == "__main__":
	print('\x1b[6;30;42m' + ' Warning - Not in Production Mode! ' + '\x1b[0m')
	app.debug = True
	app.run()
