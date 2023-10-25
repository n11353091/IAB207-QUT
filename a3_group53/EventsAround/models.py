from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(255))
    address = db.Column(db.String(255))
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    orders = db.relationship('Order', backref='user')
    events = db.relationship('Event', backref='owner')

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(80))
    type = db.Column(db.String(20))
    status = db.Column(db.String, default = "Open")
    event_date = db.Column(db.String)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    location = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    expire_date = db.Column(db.String)
    last_updated = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    #price = db.Column(db.Integer) #no need for price as it is always free
    # ... Create the Comments and Orders db.relationship
	# relation to call event.comments and comment.event
    # ... Create the Events and Orders db.relationship
	# relation to call event.orders and orders.event
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('Order', backref='event', foreign_keys='Order.event_id')
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"
    
    # *Needs to be added to sqlite db*
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    ticket_type = db.Column(db.String)
    ticket_number = db.Column(db.Integer)
    # Add event_name and event_image columns to the database
    event_name = db.Column(db.String(80))
    event_image = db.Column(db.String(400))
    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        if self.event:
            # Set event_name and event_image when an event is associated with the order
            self.event_name = self.event.name
            self.event_image = self.event.image


    # string print method
    def __repr__(self):
        return f"Order: {self.id} Booking Date: {self.created_at} Event Info: {self.event_name} Event Picture: {self.event_image}"

#Created class "Comment"
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())

    #add the foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))


    def __repr__(self):
        return "<Comment: {}>".format(self.text)