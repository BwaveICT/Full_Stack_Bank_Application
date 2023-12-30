from app import app, db
from flask import render_template, session, request, redirect, url_for, flash
from app.models.user import User, Transaction
from .reciept import generate_receipt


@app.route('/transfer', methods=['GET', 'POST'])
def transfer():
     #Retrieve user_id from session
     user_id = session.get('user_id')
     if user_id:
          user = User.query.get(user_id)


          if request.method == 'POST':
               recipient_card_name = request.form['card_name']
               recipient_card_number = request.form['card_number']
               amount = float(request.form['amount'])

               if amount > user.balance:
                    flash('Insufffient Funds', 'danger')
                    return redirect(url_for('transfer'))
               
               recipient = User.query.filter_by(card_number=recipient_card_number).first()

               if recipient and recipient.full_name == recipient_card_name:
                    #check if the reciepent is not the same as the sender
                    if recipient.id == user.id:
                         flash('Cannot send funds to yourself.', 'danger')
                         return redirect(url_for('transfer'))
                    
                    # update sender's balance
                    user.balance -= amount

                    # update recipient's balance
                    recipient.balance += amount

                    # update the database
                    db.session.commit()

                    transaction_sender = Transaction(
                         user_id=user_id,
                         recipient_name=recipient.full_name,
                         recipient_card_number=recipient.card_number,
                         amount=amount,
                         type='Debit'
                    )

                    transaction_recipient = Transaction(
                         user_id=recipient.id,
                         recipient_name=user.full_name,
                         recipient_card_number=user.card_number,
                         amount=amount,
                         type='Credit'
                    )

                    db.session.add(transaction_sender)
                    db.session.add(transaction_recipient)
                    db.session.commit()


                    # Generate reciept data
                    reciept_data = {
                         'sender_name': user.full_name,
                         'recipient_name': recipient.full_name,
                         'recipient_card_number': recipient.card_number,
                         'amount': amount
                    }

                    receipt_filename = generate_receipt(reciept_data)

                    return redirect(url_for('payment', filename=receipt_filename))
               
               else:
                    flash('Invalid recipient card name or card number.', 'danger')
                    return redirect(url_for('transfer'))



          return render_template('user/transfer.html', user=user)
     else:
          flash('You need to be log in first', 'danger')
          return redirect(url_for('login'))



