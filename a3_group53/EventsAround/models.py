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

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
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
    #price = db.Column(db.Integer) #no need for price as it is always free
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')
	
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
    event_image = db.Column(db.String(400), db.ForeignKey('events.image'))
    event_name = db.Column(db.String(80), db.ForeignKey('events.name'))
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