from app import app, bcrypt, db
from flask import render_template, request, flash, redirect, url_for, session
import random
from app.models.user import User


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        full_name = request.form['full_name']
        email = request.form['email']
        password =  request.form['password']
        confirm_password = request.form['confirm_password']
    

    # perform form validation
        
        # check if passwords match
        if password != confirm_password:
            flash('passwords do not match', 'danger')
            return redirect(url_for('register_page'))
        if len(password) < 6:
            flash('Password is too short. Please make it more lengthy', 'danger')
            return redirect(url_for('register_page'))

        
        # check if email already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('You already have an account. Please log in', 'danger')
            return redirect(url_for('login'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')


        # generate a card number
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(16) ])
        formatted_card_number = '_'.join([card_number[i:i+4] for i in range(0, len(card_number), 4)])

        # create a user
        new_user = User(full_name=full_name, email=email, password=hashed_password, card_number=card_number)
        db.session.add(new_user)
        db.session.commit()

        # store user_id and card number in session
        session['user_id'] = new_user.id
        session['card_number'] = formatted_card_number

        flash('Registration Sucessful. Welcome to our Banking Application', 'success')
        return redirect(url_for('dashboard'))
    

    return render_template('root/register.html')
