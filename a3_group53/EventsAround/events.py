from flask import Blueprint, flash, render_template, request, redirect, url_for
from .models import Event, Comment, Order
from .forms import EventForm, CommentForm, OrderForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

bp = Blueprint('event', __name__, url_prefix='/events')

@bp.route('/<id>')
def show(id):
    event = Event.query.filter_by(id=id).first()
    # create the comment form
    cform = CommentForm()    
    return render_template('events/show.html', event=event, form=cform)

@bp.route('/search')
def search():
    form = EventForm()
    events = Event.query.all()  # Fetch all events initially

    if request.method == 'POST':
        # Retrieve filter criteria from the form
        name = request.form.get('name')
        event_type = request.form.get('type')
        # Add more filter criteria if needed

        # Filter events based on the criteria
        if name:
            events = [event for event in events if name.lower() in event.name.lower()]
        if event_type:
            events = [event for event in events if event.type == event_type]

        # Redirect to the 'event.search' route within the 'event' blueprint
        return redirect(url_for('events.search'))
    return render_template('events/search.html', form=form, events=events)

@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path=check_upload_file(form)
    event=Event(name=form.name.data,
                type=form.type.data,
                event_date=form.event_date.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                location=form.location.data,
                description=form.description.data, 
                expire_date=form.expire_date.data, 
                image=db_file_path,
                )
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    try:
       db.session.add(event)
       db.session.commit()
       print('Successfully created new event', 'success')
       return redirect(url_for('event.create'))
    except Exception as e:
        db.session.rollback()
        print(f'Error creating new travel event: {str(e)}', 'error')
        print('Successfully created new travel event', 'success')
    return redirect(url_for('event.create'))  # Redirect to the 'event.create' route within the 'event' blueprint
  return render_template('events/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp=form.image.data
  filename=fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH=os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path='/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path

@bp.route('/<event>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(event):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event_obj = Event.query.filter_by(id=event).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        event=event_obj,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=event))

@bp.route('/<event>/book', methods = ['GET', 'POST'])  
@login_required
def book(event):
   form = OrderForm()
   if form.validate_on_submit():
      order = Order(
         ticket_number=form.ticket_number.data,
         ticket_type=form.ticket_type.data,
         )
      db.session.add(order) # add the object to the db session
      db.session.commit()
      return redirect(url_for('event.book')) 
   return render_template('events/book.html', form=form)

# @bp.route('/<event>/manage', methods=['GET', 'POST'])
# @login_required
# def manage(event_id):
#     event = Event.query.get(event_id)
#     form = EventForm(obj=event)  # Populate the form with the event's data

#     if form.validate_on_submit():
#         # Update the event data
#         form.populate_obj(event)
#         db.session.commit()
#         flash('Event updated successfully', 'success')
#         return redirect(url_for('event.manage', event_id=event_id))

#     return render_template('events/manage.html', form=form, event=event)