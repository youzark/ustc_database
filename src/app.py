"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, flash
from flask import render_template, request, redirect, url_for
from flask_ngrok import run_with_ngrok

from forms import LoginForm, RegisterForm, HomeForm, CommentForm, SearchForm, MessageForm
from manager import User, random_filename
from flask_login import login_user, login_required, current_user
from flask_login import LoginManager
from flask_login import logout_user

import datetime
import DB

app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"
run_with_ngrok(app)

import os
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'static')

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(user_name)
        if user.verify_password(password):
            login_user(user, remember = remember_me)
            return redirect(url_for('mainhome', name = user_name))
    return render_template('login.html', form = form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        user = User(user_name)
        user.password = password
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/home/<name>', methods=['GET','POST'])
@login_required
def home(name):
    form = HomeForm()
    if form.validate_on_submit():
        title = request.form.get('title', None)
        f = form.movie.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        DB.video_insert(title, filename, name, time)
        return redirect(url_for('video', username = name))
    return render_template('home.html', name = current_user.username, form = form)

@app.route('/othershome/<username>', methods=['GET','POST'])
@login_required
def othershome(username):
    is_friend = DB.friendship_query(current_user.username, username)
    form = MessageForm()
    if form.validate_on_submit():
        message = request.form.get('message', None)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        DB.send_eamil(current_user.username, username, message, time)
        return redirect(url_for('othershome', username = username))
    return render_template('othershome.html', name = current_user.username, username = username, is_friend = is_friend, form = form)
@app.route('/addfriend/<username>')
@login_required
def add_friend(username):
    DB.friendship_insert(current_user.username, username)
    return redirect(url_for('othershome', username = username))
@app.route('/deletefriend/<username>')
@login_required
def delete_friend(username):
    DB.friendship_delete(current_user.username, username)
    return redirect(url_for('othershome', username = username))

@app.route('/video/<username>', methods=['GET','POST'])
@login_required
def video(username):
    videos = DB.video_user_query(username)
    is_equal = username == current_user.username
    return render_template('video.html', authorname = username, username = current_user.username, videos = videos, is_equal = is_equal)

@app.route('/singlemovie/<id>', methods=['GET','POST'])
@login_required
def singlemovie(id):
    video = DB.video_id_query(id)
    comments = DB.video_comments_query(id)
    is_admin = DB.admin_name_query(current_user.username) 
    video_right = is_admin or current_user.username == video[2]
    form = CommentForm()
    if form.validate_on_submit():
        comment = request.form.get('comment', None)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        DB.video_comments_insert(id, current_user.username, comment, time)
        return redirect(url_for('singlemovie', id = id))
    return render_template('singlemovie.html', name = current_user.username, id = id, 
                           video = video, comments = comments, form = form, video_right = video_right, comment_right = is_admin)
@app.route('/deletemovie/<id>')
@login_required
def delete_movie(id):
    video = DB.video_id_query(id)
    DB.video_delete(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], video[1]))
    return redirect(url_for('video', username = video[2]))
@app.route('/deletecomment/<id>')
@login_required
def delete_comment(id):
    video_id = DB.comment_video_query(id)
    DB.comment_delete(id)
    return redirect(url_for('singlemovie', id = video_id))

@app.route('/friend/<name>', methods=['GET','POST'])
@login_required
def friend(name):
    friends = DB.friends_list_query(name)
    emails = DB.message_query(name)
    form = SearchForm()
    if form.validate_on_submit():
        name = request.form.get('name', None)
        return redirect(url_for('user_result', username = name))
    return render_template('friends.html', username = current_user.username, friends = friends, emails = emails, form = form)

@app.route('/result/<username>', methods=['GET','POST'])
@login_required
def user_result(username):
    names = DB.user_name_query(username)
    return render_template('result.html', names = names, username = current_user.username)

@app.route('/main', methods=['GET','POST'])
@login_required
def mainhome():
    form = SearchForm()
    videos = DB.video_query()
    if form.validate_on_submit():
        name = request.form.get('name', None)
        return redirect(url_for('video_result', name = name))
    return render_template('MAINHOME.html', name = current_user.username, form = form, videos = videos)

@app.route('/video_result/<name>', methods=['GET','POST'])
@login_required
def video_result(name):
    videos = DB.video_name_query(name)
    return render_template('video_result.html', videos = videos, username = current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
