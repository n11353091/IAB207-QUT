from flask import Blueprint, render_template, request, redirect,url_for
from .models import Event


mainbp = Blueprint('main', __name__)


@mainbp.route('/')
def index():
    events = Event.query.all()    
    return render_template('index.html', events=events)
    #TODO: add filtering