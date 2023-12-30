from app import app
from flask import render_template, session, flash, redirect, url_for
from app.models.user import User

@app.route('/dashboard')
def dashboard():
     # Retrieve user_id from session
     user_id = session.get('user_id')


     if user_id:
          # Retrieve the user from the db using the user_id
          user = User.query.get(user_id)
          return render_template('user/index.html', user=user)
     else:
          flash('You need to log in first to access your dashboard', 'danger')
          return redirect(url_for('login'))
     






