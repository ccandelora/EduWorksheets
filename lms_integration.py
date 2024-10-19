from flask import Blueprint, request, session, url_for
from pylti1p3.contrib.flask import FlaskOIDCLogin, FlaskMessageLaunch
from pylti1p3.tool_config import ToolConfDict
from pylti1p3.registration import Registration
from app import app
from models import User, Worksheet

lti_bp = Blueprint('lti', __name__)

class ExtendedFlaskMessageLaunch(FlaskMessageLaunch):
    def validate_nonce(self):
        """
        Probably it is bug in pylti1p3 code, but it uses `sess.setter` if flask.session is used as a session.
        This implementation uses flask.session as a dict.
        """
        nonce = self.get_launch_data().get('nonce')
        if not nonce:
            raise Exception('Nonce not found in launch data')

        if nonce not in session.get('nonces', []):
            raise Exception('Invalid Nonce')

        session['nonces'] = [n for n in session.get('nonces', []) if n != nonce]

        return self

def get_lti_config():
    return ToolConfDict({
        "http://imsglobal.org": {
            "client_id": "your_client_id",
            "auth_login_url": "https://your_lms_domain/auth",
            "auth_token_url": "https://your_lms_domain/token",
            "key_set_url": "https://your_lms_domain/keyset",
            "private_key_file": "path/to/your/private.key",
            "deployment_ids": ["your_deployment_id"]
        }
    })

@lti_bp.route('/login', methods=['GET', 'POST'])
def login():
    tool_conf = get_lti_config()
    launch_data_storage = session

    oidc_login = FlaskOIDCLogin(
        request, tool_conf, launch_data_storage=launch_data_storage
    )
    return oidc_login.enable_check_cookies().redirect(url_for('lti.launch', _external=True))

@lti_bp.route('/launch', methods=['POST'])
def launch():
    tool_conf = get_lti_config()
    launch_data_storage = session
    message_launch = ExtendedFlaskMessageLaunch(
        request, tool_conf, launch_data_storage=launch_data_storage
    )

    message_launch_data = message_launch.get_launch_data()
    user_id = message_launch_data.get('sub')
    
    # Check if the user exists, if not create a new one
    user = User.query.filter_by(lti_user_id=user_id).first()
    if not user:
        user = User(username=f"lti_user_{user_id}", lti_user_id=user_id)
        db.session.add(user)
        db.session.commit()

    # Log the user in
    login_user(user)

    # Redirect to the dashboard
    return redirect(url_for('worksheet.dashboard'))

# Add more LTI-related routes and functions as needed

app.register_blueprint(lti_bp, url_prefix='/lti')
