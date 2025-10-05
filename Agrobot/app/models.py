from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    image_class_name = db.Column(db.String(128), nullable=True)  # Maps to image class (e.g., 'Pepper_Bell_Bacterial_Spot')
    symptom_en = db.Column(db.Text)
    symptom_hi = db.Column(db.Text)
    symptom_bn = db.Column(db.Text)
    symptom_te = db.Column(db.Text)
    prevention_en = db.Column(db.Text)
    prevention_hi = db.Column(db.Text)
    prevention_bn = db.Column(db.Text)
    prevention_te = db.Column(db.Text)