from app import db
from datetime import datetime


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_name = db.Column(db.String(200))
    recipient_card_number = db.Column(db.String(16))
    amount = db.Column(db.Float)
    type = db.Column(db.String(25))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='transactions')
