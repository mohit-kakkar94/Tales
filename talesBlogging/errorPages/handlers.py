from flask import Blueprint, render_template

errorPages = Blueprint("errorPages", __name__) #"errorPages" is the name of the blueprint

@errorPages.app_errorhandler(404)
def error404(error):
    return render_template("errorPages/404.html"), 404

@errorPages.app_errorhandler(403)
def error404(error):
    return render_template("errorPages/403.html"), 403
