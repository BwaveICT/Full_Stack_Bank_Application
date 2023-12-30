from app import app, db
from flask import render_template, session, redirect, request, flash, url_for
from app.models.user import User, Transaction



@app.route('/recharge', methods=['GET', 'POST'])
def recharge():
     # Retrieve user_id from session
     user_id = session.get('user_id')
     if user_id:
          user = User.query.get(user_id)

          if request.method == 'POST':
               amount = float(request.form['amount'])

               # calculate the discount amount (10% of the recharge)
               discount = amount * 0.1
               total_amount = amount - discount

               #check if the the user has sufficent balance
               if total_amount > user.balance:
                    flash('Insufficent balance', 'danger')
                    return redirect(url_for('recharge'))
               
               #update the user's balance
               user.balance -= total_amount

               # update the database
               db.session.commit()

               transaction = Transaction(
                    user_id=user.id,
                    recipient_name=user.full_name,
                    recipient_card_number=user.card_number,
                    amount=total_amount, 
                    type="Debit - Airtime Purchase"
               )

               db.session.add(transaction)
               db.session.commit()

               return render_template('user/recharge_success.html', amount=total_amount, discount=discount)
          
          return render_template('user/recharge.html', user=user)
     else:
          flash('You need to be logged in first', 'danger')
          return redirect(url_for('login'))