from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_required, current_user
from datetime import datetime
from . import db
from .models import Author, Post

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
    
@main.route('/journal')
@login_required
def journal():
    ROWS_PER_PAGE = 10
    page = request.args.get('page', 1, type=int)

    posts = Post.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    return render_template('journal.html', posts = posts)

@main.route('/create', methods=['GET', 'POST'])
@login_required
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

            return redirect(url_for('main.index'))
    return render_template('create.html', name=current_user.name)

@main.route('/<int:id>/edit/', methods=('GET', 'POST'))
@login_required
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

            return redirect(url_for('main.index'))

    return render_template('edit.html', post=post)


@main.route('/speak', methods=('GET', 'POST'))
@login_required
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

            return redirect(url_for('main.index'))
    return render_template('speak.html')
