from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect database to Flask app"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """model for a user"""

    __tablename__="users"

    username = db.Column(db.String(20), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship("Feedback", backref="user", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user and hash their password"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls,username,password):
        """validate the username and password upon login"""

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False
        

class Feedback(db.Model):
    """model for feedback Users can create or delete"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.String(20), db.ForeignKey("users.username"), nullable=False)