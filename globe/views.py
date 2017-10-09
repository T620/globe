import os
from globe import app, db
from flask import render_template, request, redirect, url_for, session, abort


@app.route('/')
def load_index():
	return render_template("index.html")




if __name__ == '__app__':
	app.debug=True
	app.run(host='0.0.0.0', port=5000)
