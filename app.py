import re
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, Response
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import exc

app = Flask(__name__)

# https://medium.com/analytics-vidhya/how-to-rate-limit-routes-in-flask-61c6c791961b#:~:text=Rate%20Limiting%20allows%20you%20to,exempt%20to%20have%20no%20limits.
# Rate limiting

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None: raise Exception("Database URL was not defined")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize ORM
db = SQLAlchemy(app)

# Init marshmallow
ma = Marshmallow(app)

# To create tables, run:
# db.create_all()


class Game(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	result = db.Column(db.String(4), nullable=False)

	def __repr__(self):
		return json.dumps({"id": self.id, "date": self.date, "name": self.name })

# Instructs how to return the object as JSON
class GameSchema(ma.Schema):
	class Meta:
		fields = ('id', 'result', 'date')

game_schema = GameSchema()
games_schema = GameSchema(many=True)

@app.route('/score', methods=['POST'])
def createGame():
	try:
		print(request.json)
		result = request.json['result']
		print(result)
		if not re.match(r"^(Win|Loss|Draw)$", result): print('Invalid')
		newGame = Game(result=result)
		db.session.add(newGame)
		db.session.commit()
		x = game_schema.jsonify(newGame)
		return x, 201
	except Exception as e:
		print(e)
		return Response(f"Invalid Request: {e}" , status=400)


@app.route('/score', methods=['GET'])
def getGames():
	allGames = Game.query.all()
	return games_schema.jsonify(allGames)


if __name__ == "__main__":
	print('\x1b[6;30;42m' + ' Warning - Not in Production Mode! ' + '\x1b[0m')
	app.debug = True
	app.run()
