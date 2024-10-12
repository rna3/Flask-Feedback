from flask import Flask, redirect, render_template, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secretfeedback"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    # db.drop_all()
    db.create_all()


@app.route("/")
def index():
    """ return a redirect to "/register" """

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register_user():
    """show register form on get request, and handle form submission for post request"""
    
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        user = User.register(username, password, email, first_name, last_name)

        db.session.commit()

        session['username'] = user.username
        
        return redirect(f"/user/{user.username}")
    
    else:

        return render_template("user_register_form.html", form=form)
    

@app.route("/user/<username>")
def user_page(username):
    """show the user page but first check the session for logged in status"""

    if "username" not in session or username != session['username']:
        return redirect("/login")
    
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("user_page.html", user=user, form=form)


@app.route("/login", methods=["GET", "POST"])
def login_form():
    """show the login form"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/user/{user.username}")
        else:
            form.username.errors = ["Wrong Username or Password"]
            return render_template("login_form.html", form=form)

    return render_template("/login_form.html", form=form)


@app.route("/logout")
def logout():
    """route to log a user out of the site"""

    session.pop("username")
    return redirect("/login")

@app.route("/user/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """show the add-feedback-form upon GET request"""

    if "username" not in session or username != session['username']:
        return redirect("/login")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/user/{feedback.username}")
    
    else:
        return render_template("add_feedback_form.html", form=form)
    

@app.route("/feedback/<int:feedback_id>/edit", methods=["GET", "POST"])
def edit_feedback(feedback_id):
    """show the form to edit the content and title"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect("/login")
    
    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/user/{feedback.username}")
    
    return render_template("feedback_edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """delete the feedback created by the user"""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        return redirect("/login")
    
    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/user/{feedback.username}")


@app.route("/user/<username>/delete", methods=["POST"])
def delete_user(username):
    """delete a user account"""

    user = User.query.get(username)

    if "username" not in session or user.username != session['username']:
        return redirect("/login")
    
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")



