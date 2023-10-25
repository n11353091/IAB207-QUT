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


from flask_login import current_user  # ensure you've imported this


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    print('Method type: ', request.method)
    form = EventForm()
    if form.validate_on_submit():
        # Call the function that checks and returns image
        db_file_path = check_upload_file(form)

        # Include owner_id when creating the event
        event = Event(name=form.name.data,
                      type=form.type.data,
                      event_date=form.event_date.data,
                      start_time=form.start_time.data,
                      end_time=form.end_time.data,
                      location=form.location.data,
                      description=form.description.data,
                      expire_date=form.expire_date.data,
                      image=db_file_path,
                      owner_id=current_user.id  # Set the owner of the event
                      )
        # Add the object to the db session and commit to the database
        try:
            db.session.add(event)
            db.session.commit()
            print('Successfully created new event', 'success')
            return redirect(url_for('event.create'))
        except Exception as e:
            db.session.rollback()
            print(f'Error creating new travel event: {str(e)}', 'error')
            print('Successfully created new travel event',
                  'success')  # This seems odd. If there's an error, why print a success message?

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

@bp.route('/<id>/comment', methods = ['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event =  db.session.scalar(db.select(Event).where(Event.id==id)) 
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        event=event,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))

@bp.route('/<id>/book', methods = ['GET', 'POST'])  
@login_required
def book(id):
   form = OrderForm()
   #get the order object associated to the user and the event
   event = Event.query.get(id)
   if form.validate_on_submit():
      order = Order(
         ticket_number=form.ticket_number.data,
         ticket_type=form.ticket_type.data,
         event=event,
         user=current_user
         )
      db.session.add(order) # add the object to the db session
      db.session.commit()
      return redirect(url_for('event.book',id=id)) 
   return render_template('events/book.html', form=form)


@bp.route('/<int:event_id>/delete', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)

    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted.', 'success')
    return redirect(url_for('main.index'))
@bp.route('/<int:event_id>/manage', methods=['GET', 'POST'])
@login_required
def manage(event_id):
    event = Event.query.get_or_404(event_id)
    form = EventForm()

    # Check event ownership
    if current_user.id != event.owner_id:
        flash('You do not have permission to manage this event.', 'danger')
        return redirect(url_for('main.index'))

    if request.method == 'GET':
        # Populate the form fields with the existing event data
        populate_form_with_event_data(form, event)

    elif form.validate_on_submit():
        # Update the event attributes with the form data
        update_event_from_form(event, form)
        try:
            db.session.commit()
            flash('Event updated successfully', 'success')
            return redirect(url_for('event.details', event_id=event_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating the event: {str(e)}', 'error')
            return redirect(url_for('events.manage', event_id=event_id))

    return render_template('events/manage.html', form=form, event=event)


from datetime import datetime

def populate_form_with_event_data(form, event):
    form.name.data = event.name
    form.type.data = event.type
    form.status.data = event.status
    form.event_date.data = datetime.strptime(event.event_date, "%Y-%m-%d").date() if isinstance(event.event_date, str) else event.event_date
    form.start_time.data = event.start_time
    form.end_time.data = event.end_time
    form.location.data = event.location
    form.description.data = event.description
    form.expire_date.data = datetime.strptime(event.expire_date, "%Y-%m-%d").date() if isinstance(event.expire_date, str) else event.expire_date
    # Note: you may need additional logic for the image field

    # Note: you may need additional logic for the image field


def update_event_from_form(event, form):
    event.name = form.name.data
    event.type = form.type.data
    event.status = form.status.data
    event.event_date = form.event_date.data
    event.start_time = form.start_time.data
    event.end_time = form.end_time.data
    event.location = form.location.data
    event.description = form.description.data
    event.expire_date = form.expire_date.data
    # Handle the image logic here if necessary


