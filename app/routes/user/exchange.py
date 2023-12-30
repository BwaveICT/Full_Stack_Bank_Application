from app import app
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User

@app.route('/exchange_rate')
def exchange_rate():
     # Retrieve user_id from session
     user_id = session.get('user_id')

     if user_id:
          user = User.query.get(user_id)
          return render_template('user/soon.html', user=user)
     else:
          flash('You need to be logged in first', 'danger')
          return redirect(url_for('login'))