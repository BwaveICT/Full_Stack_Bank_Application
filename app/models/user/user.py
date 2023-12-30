from app import app, db
import re

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    card_number = db.Column(db.String(16), unique=True)
    balance = db.Column(db.Float, default=50000.00)



def insert_hyphens(value):
    value = re.sub(r'\s', '', value) # Remove any existing whitespace
    return re.sub(r'\d{4}(?!$)', '\\g<0>-', value)

app.jinja_env.filters['insert_hyphens'] = insert_hyphens