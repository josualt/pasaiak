import os
import sqlite3
from random import randint
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
    id = randint(100, 10000000)
    print(f'{name}, {description}')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(
        f"insert into homework values({id}, '{name}', '{description}')")
    conn.commit()
    return render_template('index.html')


@app.route('/homework/delete/<id>')
def homework_delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    values = conn.execute('DELETE FROM homework where id = ' + id).fetchall()
    conn.commit()
    print(f"See: {values}")
    return render_template('index.html')


@app.route('/homework/update/<id>', methods=["GET"])
def homework_update(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    value = conn.execute('select * FROM homework where id = ' + id).fetchall()
    print(f"See: {value}")
    return render_template('homework/update.html', homework=value[0])


@app.route('/homework/update', methods=["POST"])
def homework_save_update():
    id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    value = conn.execute(f"update homework set name='{name}', description='{
                         description}' where id ={id} ").fetchall()
    conn.commit()
    print(f"See: {value}")
    return render_template('index.html')


@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')


if __name__ == "__main__":
    app.run(port=port)
