from crypt import methods
from datetime import datetime
from email.policy import default
from multiprocessing import connection
from flask import Flask, render_template, request, url_for, flash, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import TIMESTAMP, insert
from sqlalchemy import Column, Integer, DateTime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/database'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'k3n%L$knn(9()wl_-o'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.Text, nullable=False) 
    content = db.Column(db.Text, nullable=False)
    init_mood = db.Column(db.SmallInteger)
    final_mood = db.Column(db.SmallInteger)


def __repr__(self):
    return '<Post %r>' % self.content


# def get_db_connection():
#     conn = sqlite3.connect('db/database.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# def get_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM post WHERE id = ?',
#                             (post_id,)).fetchone()
#     conn.close()
#     if post is None:
#         abort(404)
#     return post

@app.route('/')
def index():
    ROWS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)

    posts = Post.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('index.html', posts = posts)

@app.route('/speak', methods=('GET', 'POST'))
def speak():
    if request.method == 'POST':
        init_mood = request.form.get('imood')
        title = request.form['title']
        content = request.form['content']
        final_mood = request.form.get('pmood')

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        elif not init_mood:
            flash('How were you feeling before writing?')
        elif not final_mood:
            flash('How were you feeling after writing?')
        else:

            new_add = Post(title=title, content=content, init_mood=init_mood, final_mood=final_mood)
            db.session.add(new_add)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('speak.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        init_mood = request.form.get('imood')
        title = request.form['title']
        content = request.form['content']
        final_mood = request.form.get('pmood')
        
        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        elif not init_mood:
            flash('How were you feeling before writing?')
        elif not final_mood:
            flash('How were you feeling after writing?')
        else:

            new_add = Post(title=title, content='created: ' + str(datetime.now()) + ' -- ' + content, init_mood=init_mood, final_mood=final_mood)
            db.session.add(new_add)
            db.session.commit()

            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
def edit(id):
    post = db.session.query(Post).get(id)

    if request.method == 'POST':
        init_mood = request.form.get('imood')
        title = request.form['title']
        content = request.form['content']
        final_mood = request.form.get('pmood')

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        elif not init_mood:
            flash('How were you feeling before writing?')
        elif not final_mood:
            flash('How were you feeling after writing?')
        else:
            post.title = title
            post.content = content
            post.init_mood = init_mood
            post.final_mood = final_mood
            db.session.commit()
            
            new_add = Post(title=title, content=content + ' -- edited: ' + str(datetime.now()), init_mood=init_mood, final_mood=final_mood)
            db.session.add(new_add)
            db.session.commit()

            return redirect(url_for('index'))

    return render_template('edit.html', post=post)



@app.route('/grateful', methods=('GET', 'POST'))
def grateful():

    if request.method == 'POST':
        init_mood = request.form.get('imood')
        title = request.form['title']
        content = request.form['content']
        final_mood = request.form['pmood']

        if not title:
            flash('Title is required!')
        elif not content:
            flash('Content is required!')
        else:


            new_add = Post(title=title, content=content, init_mood=init_mood, final_mood=final_mood)
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
