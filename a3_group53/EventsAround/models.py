from flask_login import UserMixin
from . import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    types = db.column(db.String(20))
    event_date = db.Column(db.DateTime.date)
    start_time = db.column(db.DateTime.time)
    end_time = db.column(db.DateTime.time)
    location = db.column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    expire_date = db.Column(db.DateTime.date)
    price = db.Column(db.Integer)
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')
	
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    event_price = db.Column(db.Integer, db.ForeignKey('events.price'))
    event_image = db.Column(db.String(400), db.ForeignKey('events.image'))
    event_name = db.Column(db.String(80), db.ForeignKey('events.name'))
    # string print method
    def __repr__(self):
        return f"Order: {self.id} Booking Date: {self.created_at} Event Info: {self.event_name} Event Picture: {self.event_image}"