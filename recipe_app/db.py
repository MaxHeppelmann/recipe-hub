from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

# Initialize SQLAlchemy without binding to an app yet
db = SQLAlchemy()

class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False, unique=False)
    auth_cookie = db.Column(db.String(36), unique=True, nullable=True)


from sqlalchemy.dialects.postgresql import ARRAY

class recipes(db.Model):
    __tablename__ = "recipes"
    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, description: {self.description}, ingredients: {self.ingredients}, steps: {self.steps}, user_id: {self.user_id}"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    ingredients = db.Column(ARRAY(db.String(500)), nullable=False)
    steps = db.Column(ARRAY(db.String(500)), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


def init_app(app):
    """Initialize the database with the app"""
    db.init_app(app)
    
    # Create a CLI command for initializing the database
    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        with app.app_context():
            db.create_all()
            print('Database initialized.')
