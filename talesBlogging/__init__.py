import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

#Set up Flask application
app = Flask(__name__)

#Set secret key for forms
app.config["SECRET_KEY"] = "mysecret"

##################################################
                #Set up database#
##################################################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

##################################################
                #Login configurations#
##################################################
loginManager = LoginManager()

loginManager.init_app(app)

loginManager.login_view = "users.login"

#Register blueprint in talesBlogging/core/views.py
from talesBlogging.core.views import core
app.register_blueprint(core)

#Register blueprint in talesBlogging/errorPages/handlers.py
from talesBlogging.errorPages.handlers import errorPages
app.register_blueprint(errorPages)

#Register blueprint in talesBlogging/users/views.py
from talesBlogging.users.views import users
app.register_blueprint(users)

#Register blueprint in talesBlogging/blogs/views.py
from talesBlogging.blogs.views import blogPosts
app.register_blueprint(blogPosts)
