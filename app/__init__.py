from flask import Flask
from flask_socketio import SocketIO
from config import Config

socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    socketio.init_app(app)

    return app
