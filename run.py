from src.main.server.server import app, socketio
from src.main.routes.routes import main_bp


if __name__ == "__main__":
    app.register_blueprint(main_bp)
    #db_connection_handler.connect()
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

