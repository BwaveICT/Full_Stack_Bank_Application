from app import app, db
from flask import render_template, session, request, redirect, url_for, flash
from app.models.user import User, Transaction

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     if user_id:
          user = User.query.get(user_id)

          if request.method == 'POST':
               card_number = request.form['card_number']
               amount = float(request.form['amount'])

               # check if the card number matches with the user's card number
               if card_number != user.card_number:
                    flash('Invalid card number', 'danger')
                    return redirect(url_for('deposit'))
               
               # update the user's balance
               user.balance += amount

               #create a credit transaction record
               transaction = Transaction(
                    user_id=user.id,
                    recipient_name=user.full_name,
                    recipient_card_number=user.card_number,
                    amount=amount,
                    type="Credit - Deposit"
               )

               db.session.add(transaction)
               db.session.commit()
               
               flash(f'Successfully deposited ₦{amount:.2f} to your account.', 'success')
               return redirect(url_for('dashboard'))
          
          return render_template('user/deposit.html', user=user)
     else:
          flash('You need to be logged in first', 'danger')
          return redirect(url_for('login'))
