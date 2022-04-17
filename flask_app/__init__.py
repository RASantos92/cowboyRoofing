from flask import Flask
from werkzeug.utils import secure_filename
app = Flask(__name__)  
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key ="keysToDaWhip"