from datetime import datetime
from email.policy import default
from multiprocessing import connection
import sqlite3
from turtle import title
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, insert
from sqlalchemy import Column, Integer, DateTime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'k3n%L$knn(9()wl_-o'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.Text, nullable=False) 
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.content


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM post WHERE id = ?',
                         (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post

@app.route('/')
def index():

    ROWS_PER_PAGE = 5
    page = request.args.get('page', 1, type=int)

    posts = Post.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('index.html', posts = posts)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:

            new_add = Post(title=title, content=content)
            db.session.add(new_add)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = db.session.query(Post).get(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')

        elif not content:
            flash('Content is required!')

        else:
            post.title = title
            post.content = content
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)

@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM post WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/grateful', methods=('GET', 'POST'))
def grateful():

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:


            new_add = Post(title=title, content=content)
            db.session.add(new_add)
            db.session.commit()

            # conn = get_db_connection()
            # conn.execute('INSERT INTO post (title, content) VALUES (?, ?)',
            #              (title, content))
            # conn.commit()
            # conn.close()
            return redirect(url_for('index'))
    return render_template('grateful.html')


if __name__ == '__main__':
    app.run(debug= True, port = 5000)