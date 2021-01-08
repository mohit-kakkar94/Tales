from flask import Flask

#Set up Flask application
app = Flask(__name__)

#Register blueprint in talesBlogging/core/views.py
from talesBlogging.core.views import core
app.register_blueprint(core)
