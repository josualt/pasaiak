import os
import sqlite3
from random import randint
from flask import Flask, send_from_directory, render_template, redirect, request, session

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))
app.secret_key = 'BAD_SECRET_KEY'


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
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    values = conn.execute('SELECT * FROM subject').fetchall()
    return render_template('homework/new.html', subjects=values)


@app.route('/subjects/new')
def subject_new():
    return render_template('subjects/new.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=["POST"])
def check_login():
    email = request.form['email']
    password = request.form['password']
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    print(email, password)
    result = cursor.execute(
        f"select * from users  where email = '{email}' and password = '{password}'").fetchall()
    print(f"{result}")
    if result and result[0][0] is not None:
        session['user'] = result[0][0]
        return redirect('/homework')
    else:
        return render_template('login.html', mezu='Pasahitza desegokia')


@app.route('/homework')
def homework_index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    values = conn.execute(
        'SELECT homework.*, subject.name  as subject FROM "homework" inner join subject on subject.id = homework.id_subject').fetchall()
    print(f"See: {values}")
    return render_template('homework/index.html', homeworks=values)


@app.route('/homework/save', methods=["POST"])
def homework_save():
    name = request.form['name']
    description = request.form['description']
    id_subject = request.form['id_subject']
    id = randint(100, 10000000)
    print(f'{name}, {description}')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(
        f"insert into homework values({id}, '{name}', '{description}', {id_subject})")
    conn.commit()
    return render_template('index.html')


@app.route('/subjects/save', methods=["POST"])
def subject_save():
    name = request.form['name']
    id = randint(100, 10000000)
    print(f'{name}, {id}')
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(
        f"insert into subject values({id}, '{name}')")
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


@app.route('/subjects/delete/<id>')
def subjects_delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    values = conn.execute('DELETE FROM subject where id = ' + id).fetchall()
    conn.commit()
    print(f"See: {values}")
    return render_template('index.html')


@app.route('/homework/update/<id>', methods=["GET"])
def homework_update(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    value = conn.execute('select * FROM homework where id = ' + id).fetchall()
    print(f"See: {value}")
    values = conn.execute('SELECT * FROM subject').fetchall()
    return render_template('homework/update.html', homework=value[0], subjects=values)


@app.route('/subjects/update/<id>', methods=["GET"])
def subject_update(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    value = conn.execute('select * FROM subject where id = ' + id).fetchall()
    print(f"See: {value}")
    return render_template('subjects/update.html', subject=value[0])


@app.route('/homework/update', methods=["POST"])
def homework_save_update():
    id = request.form['id']
    name = request.form['name']
    description = request.form['description']
    id_subject = request.form['id_subject']
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    value = conn.execute(f"update homework set name='{name}', description='{
                         description}' ,id_subject={id_subject} where id ={id} ").fetchall()
    conn.commit()
    print(f"See: {value}")
    return render_template('index.html')


@app.route('/subjects/update', methods=["POST"])
def subject_save_update():
    id = request.form['id']
    name = request.form['name']
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    value = conn.execute(f"update subject set name='{
                         name}' where id ={id} ").fetchall()
    conn.commit()
    print(f"See: {value}")
    return render_template('index.html')


@app.route('/subjects')
def subject_index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    values = conn.execute('SELECT * FROM subject').fetchall()
    print(f"See: {values}")
    return render_template('subjects/index.html', subjects=values)


@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')


if __name__ == "__main__":
    app.run(port=port)
