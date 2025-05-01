from flask import Blueprint, jsonify
from services import *

# Create a Blueprint
routes_bp = Blueprint('routes', __name__)

# Create a test route
@routes_bp.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Server is running'})

# Get Complaint Statistics
@routes_bp.route('/api/grievance/stats', methods=['GET'])
def get_complaint_stats():
    return get_complaint_stats_service()

# Create a complaint
@routes_bp.route('/api/grievance/new_complaint', methods=['POST'])
def create_complaint_route():
    if request.content_type and 'multipart/form-data' in request.content_type:
        data = {
            'user_id': request.form.get('user_id'),
            'complaint_message': request.form.get('description'),
            'complaint_title': request.form.get('title'),
            'image_file': request.files.get('image_file') if 'image_file' in request.files else None
        }

        print("Data from form:", data)
    else:
        data = request.get_json()
    return create_complaint_service(data)

# get all complaints
@routes_bp.route('/api/grievance/complaints', methods=['GET'])
def get_all_complaint_route():
    return get_all_complaint_service()

# get complaint by id
@routes_bp.route('/api/grievance/complaint/<c_id>', methods=['GET'])
def get_complaint_route(c_id):
    return get_complaint_service(c_id)

# Upvote a complaint
@routes_bp.route('/api/grievance/upvote/<c_id>', methods=['PUT'])
def upvote_complaint_route(c_id):
    return upvote_complaint_service(c_id)

# Downvote a complaint
@routes_bp.route('/api/grievance/downvote/<c_id>', methods=['PUT'])
def downvote_complaint_route(c_id):
    return downvote_complaint_service(c_id)

# Get number of upvotes for a complaint
@routes_bp.route('/api/grievance/get_upvotes/<c_id>', methods=['GET'])
def get_upvotes_route(c_id):
    return get_upvotes_service(c_id)

# Add a resolver to a complaint
@routes_bp.route('/api/grievance/add_resolver/<c_id>', methods=['PUT'])
def add_resolver_route(c_id):
    return add_resolver_service(c_id)

# Add Comment to a complaint
@routes_bp.route('/api/grievance/add_comment/<c_id>', methods=['POST'])
def add_comment_route(c_id):
    return add_comment_service(c_id)

# Get all comments for a complaint
@routes_bp.route('/api/grievance/get_comments/<c_id>', methods=['GET'])
def get_comments_route(c_id):   
    return get_comments_service(c_id)

# Delete a comment from a complaint
@routes_bp.route('/api/grievance/delete_comment/<c_id>/<comment_id>', methods=['DELETE'])
def delete_comment_route(c_id, comment_id):
    return delete_comment_service(c_id, comment_id)

# Delete a complaint
@routes_bp.route('/api/grievance/delete_complaint/<c_id>', methods=['DELETE'])
def delete_complaint_route(c_id):
    return delete_complaint_service(c_id)
