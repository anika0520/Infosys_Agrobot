from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import tensorflow as tf
import os
app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load TensorFlow model
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.h5')
if os.path.exists(model_path):
    tf_model = tf.keras.models.load_model(model_path)
else:
    tf_model = None  
from app import routes  