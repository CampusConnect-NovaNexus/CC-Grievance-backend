from flask import Blueprint
from AI_Services import *

# Create a Blueprint
ai_routes_bp = Blueprint('ai_routes', __name__)

# -------- AI Services APIs --------

@ai_routes_bp.route("/api/grievance/ai/embed_store", methods=["POST"])
def embed_store():
    return embed_service()

@ai_routes_bp.route("/api/grievance/ai/query", methods=["POST"])
def query():
    return query_service()
