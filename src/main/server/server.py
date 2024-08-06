from flask import Flask
from src.main.routes.routes import main_bp

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.register_blueprint(main_bp)