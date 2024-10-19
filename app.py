import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or "a_very_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# LTI Configuration
app.config['LTI_TOOL_CONFIG'] = {
    "http://imsglobal.org": {
        "client_id": os.environ.get("LTI_CLIENT_ID"),
        "auth_login_url": os.environ.get("LTI_AUTH_LOGIN_URL"),
        "auth_token_url": os.environ.get("LTI_AUTH_TOKEN_URL"),
        "key_set_url": os.environ.get("LTI_KEY_SET_URL"),
        "private_key_file": os.environ.get("LTI_PRIVATE_KEY_FILE"),
        "deployment_ids": [os.environ.get("LTI_DEPLOYMENT_ID")]
    }
}

db.init_app(app)
login_manager.init_app(app)
migrate.init_app(app, db)
login_manager.login_view = 'auth.login'

with app.app_context():
    from models import User, Worksheet, WorksheetTemplate

from auth import auth_bp
from worksheet_generator import worksheet_bp
from lms_integration import lti_bp
from ai_question_generator import ai_question_bp

app.register_blueprint(auth_bp)
app.register_blueprint(worksheet_bp)
app.register_blueprint(lti_bp, url_prefix='/lti', name='lti_blueprint')
app.register_blueprint(ai_question_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
