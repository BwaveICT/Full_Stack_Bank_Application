from app import app
from flask import render_template, session, redirect, flash, url_for
from app.models.user import User, Transaction


@app.route('/transaction_history')
def transaction_history():
    user_id = session.get('user_id')
        
    if user_id:
        user = User.query.get(user_id)

        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.timestamp.desc()).all()

        return render_template('user/transaction_history.html', user=user, transactions=transactions)
    else:
        flash('You need to log in first', 'danger')
        return redirect(url_for('login'))
   
  