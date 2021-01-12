from flask import render_template, request, Blueprint
from talesBlogging.models import BlogPost

core = Blueprint("core", __name__) #"core" (in parentheses) is the name of the blueprint

@core.route("/")
def index():

    page = request.args.get("page", 1, type=int)
    blogPosts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)

    return render_template("index.html", blogPosts=blogPosts)

@core.route("/info")
def info():
    return render_template("info.html")
