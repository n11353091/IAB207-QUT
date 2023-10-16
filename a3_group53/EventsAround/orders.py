from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import EventForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required

bp = Blueprint('order', __name__, url_prefix='/orders')

@bp.route('/history', methods = ['GET', 'POST'])
@login_required
def history():
  return render_template('orders/history.html')

@bp.route('/confirmation', methods = ['GET', 'POST'])
@login_required
def confirmation():
  return