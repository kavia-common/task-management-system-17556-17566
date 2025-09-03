from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from .routes.health import blp as health_blp
from .routes.tasks import blp as tasks_blp
from .models import init_db

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})

# OpenAPI / API docs configuration
app.config["API_TITLE"] = "To-Do API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/docs"
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

api = Api(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(tasks_blp)

# Initialize the database at app startup
with app.app_context():
    init_db()
