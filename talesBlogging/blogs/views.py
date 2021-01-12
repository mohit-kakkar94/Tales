from flask import render_template, url_for, request, redirect, Blueprint
from flask_login import current_user, login_required
from talesBlogging import db
from talesBlogging.models import BlogPost
from talesBlogging.blogs.forms import BlogPostForm

blogPosts = Blueprint("blogPosts", __name__)

@blogPosts.route("/create", methods=["GET", "POST"])
@login_required
def createPost():

    form = BlogPostForm()

    if form.validate_on_submit():

        blogPost = BlogPost(title=form.title.data, text=form.text.data, userId=current_user.id)
        db.session.add(blogPost)
        db.session.commit()

        return redirect(url_for("core.index"))

    return render_template("createPost.html", form=form)

@blogPosts.route("/<int:blogPostId>")
def blogPost(blogPostId):

    blogPost = BlogPost.query.get_or_404(blogPostId)
    return render_template("blogPost.html", title=blogPost.title, date=blogPost.date, post=blogPost)

@blogPosts.route("/<int:blogPostId>/update", methods=["GET", "POST"])
@login_required
def update(blogPostId):

    blogPost = BlogPost.query.get_or_404(blogPostId)

    if blogPost.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():

        blogPost.title = form.title.data
        blogPost.text = form.text.data
        db.session.commit()

        return redirect(url_for("blogPosts.blogPost", blogPostId=blogPost.id))

    elif request.method == "GET":
        form.title.data = blogPost.title
        form.text.data = blogPost.text

    return render_template("createPost.html", title="Updating", form=form)

@blogPosts.route("/<int:blogPostId>/delete", methods=["GET", "POST"])
@login_required
def deletePost(blogPostId):

    blogPost = BlogPost.query.get_or_404(blogPostId)

    if blogPost.author != current_user:
        abort(403)

    db.session.delete(blogPost)
    db.session.commit()

    return redirect(url_for("core.index"))
