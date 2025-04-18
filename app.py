import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from waitress import serve
from flask_migrate import Migrate
from routes import routes_bp
from AI_routes import ai_routes_bp

load_dotenv()

app = Flask(__name__)
CORS(app) 

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').strip()

from models import db
migrate = Migrate(app, db)

# Initialize the app with SQLAlchemy
db.init_app(app)

# Register blueprints for routes
app.register_blueprint(routes_bp)
app.register_blueprint(ai_routes_bp)

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=4000)