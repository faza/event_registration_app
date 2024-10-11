from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.models import User, Event
from datetime import datetime

def index():
    return render_template('base.html')

def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.get_user_by_username(username):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.get_user_by_email(email):
            flash('Email already exists')
            return redirect(url_for('register'))

        user = User.create_user(username, email, password)
        flash('Registration successful')
        return redirect(url_for('login'))

    return render_template('register.html')

def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.get_user_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect(url_for('index'))

@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        date_str = request.form.get('date')
        location = request.form.get('location')

        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')

        event = Event.create_event(title, description, date, location, current_user.id)
        flash('Event created successfully')
        return redirect(url_for('list_events'))

    return render_template('create_event.html')

def list_events():
    events = Event.get_all_events()
    return render_template('list_events.html', events=events)

@login_required
def event_details(event_id):
    event = Event.get_event_by_id(event_id)
    if event:
        return render_template('event_details.html', event=event)
    flash('Event not found')
    return redirect(url_for('list_events'))
