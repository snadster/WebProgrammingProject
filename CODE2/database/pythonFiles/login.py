from flask_login import LoginManager

from pythonFiles import user # circular import

login_manager = LoginManager()

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    # throw people who aren't logged in to the fron page if they try to access something
    login_manager.login_view = "frontpage" 

@login_manager.user_loader
# creative name i know. Checks if user exists in database
def load_user(user_id):
    return user.User.get_by_id(user_id)