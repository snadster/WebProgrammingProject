
from flask import Flask


# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Import the views, except its mad at me when i do so
import views

#for bugfixing yip
# with app.app_context():
#     db.drop_all()
#     db.create_all()
