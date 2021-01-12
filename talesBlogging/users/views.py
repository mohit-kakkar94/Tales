from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from talesBlogging import db
from talesBlogging.models import User, BlogPost
from talesBlogging.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from talesBlogging.users.pictureHandler import addProfilePic

users = Blueprint("users", __name__)

@users.route("/Sign up", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():

        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)

@users.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.checkPassword(form.password.data):

            login_user(user)

            #For the case where user was earlier trying to visit a page that requires login
            next = request.args.get("next")

            if next == None or not next[0] == "/":
                next = url_for("core.index")

            return redirect(next)

    return render_template("login.html",form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = addProfilePic(form.picture.data, username)
            current_user.profileImage = pic

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profileImage = url_for("static", filename="profilePics/" + current_user.profileImage)

    return render_template("account.html", profileImage=profileImage, form=form)

@users.route("/<username>")
def userPosts(username):

    page = request.args.get("page", 1, type=int) #cycle through posts through pages
    user = User.query.filter_by(username=username).first_or_404() #Grab the user or if there is no user then grab the 404
                                                                 #page
    blogPosts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    #author is backref for the relationship between User and BlogPost

    return render_template("userBlogPosts.html", blogPosts=blogPosts, user=user)
