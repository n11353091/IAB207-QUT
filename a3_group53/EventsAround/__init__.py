#from package import Class
from flask import Flask, render_template 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db=SQLAlchemy()
app=Flask(__name__)

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='somesecretgoeshere'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///mydbname.sqlite'
    #initialise db with flask app
    db.init_app(app)

    bootstrap = Bootstrap5(app)
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a common practice.
    from . import views
    app.register_blueprint(views.mainbp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import events
    app.register_blueprint(events.bp)

    from . import orders
    app.register_blueprint(orders.bp)

    return app

@app.errorhandler(400) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("errors/400.html"), 400

@app.errorhandler(401)
# inbuilt function which takes error as parameter
def unauthorized(e):
    return render_template("errors/401.html"), 401

@app.errorhandler(403)
def forbidden(e):
    return render_template("errors/403.html"), 403

@app.errorhandler(404) 
# inbuilt function which takes error as parameter 
def not_found(e): 
  return render_template("errors/404.html"), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("errors/405.html"), 405

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500

@app.errorhandler(503)
def service_unavailable(e):
    return render_template("errors/503.html"), 503