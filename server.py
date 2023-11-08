import os
import sqlite3
from flask import Flask, send_from_directory, render_template, redirect, request

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/homework/new')
def homework_new():
    return render_template('homework/new.html')


@app.route('/homework')
def homework_index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    values = conn.execute('SELECT * FROM homework').fetchall()
    print(f"See: {values}")
    return render_template('homework/index.html', homeworks=values)


@app.route('/homework/save', methods=["POST"])
def homework_save():
    name = request.form['name']
    description = request.form['description']
    print(f'{name}, {description}')
    return render_template('homework/new.html')


@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')


if __name__ == "__main__":
    app.run(port=port)
