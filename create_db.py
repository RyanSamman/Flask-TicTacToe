from app import db

# Run this file once to create the tables inside your database
if __name__ == "__main__":
	db.create_all()
	print('Database(s) created!')