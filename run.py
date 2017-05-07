from app import app
import os

if __name__ == '__main__':	
	app.run(host='localhost', port=8080, debug=True, reloader=True)