
# login.py


from flask_login import LoginManager


login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_uuid):

    from flaskr_carved_rock.models.user import User
    return User.query.filter_by(uuid=user_uuid).first()


@login_manager.request_loader
def load_user_from_request(request):

    from flaskr_carved_rock.models.user import User
    api_key = request.headers.get('x-api-key')
    if api_key:

        user = User.query.filter_by(api_key=api_key).first()

        if user:
            
            return user
        
    return None
