from flask import Blueprint, render_template, request, redirect,url_for
from .models import Event
mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = Event.query.all()    
    return render_template('index.html', events=events)
    #TODO: add filtering

@mainbp.route('/search')
def search():
    if request.args['search']:
        print(request.args['search'])
        evnt = "%" + request.args['search'] + '%'
        event = Event.query.filter(Event.description.like(evnt)).all()
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
    #TODO: add filtering