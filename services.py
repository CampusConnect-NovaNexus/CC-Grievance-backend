from flask import request, jsonify, make_response
from models import db, Complaint, Comment, ComplaintStats

# Modify your create_complaint_service function to increment total_created
def create_complaint_service():
    try:
        data = request.get_json()
        new_complaint = Complaint(user_id=data['user_id'], complaint_message=data['description'], complaint_title = data['title'])
        db.session.add(new_complaint)
        
        # Update stats before committing the transaction
        stats = ComplaintStats.query.first()
        if not stats:
            stats = ComplaintStats(total_created=1, total_resolved=0)
            db.session.add(stats)
        else:
            stats.total_created += 1
        
        # Commit all changes in a single transaction
        db.session.commit()
        
        # Return the response
        return jsonify(new_complaint.json()), 201
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return make_response(jsonify({'message' : "error creating complaint", 'error' : str(e)}), 500)

# Get all complaints
def get_all_complaint_service():
    try:
        complaints = Complaint.query.all()

        # Return your existing response
        return make_response(jsonify({'complaints' : [complaint.json() for complaint in complaints]}), 200)
    except Exception as e:
        return make_response(jsonify({'message' : "error getting complaints", 'error' : str(e)}), 500)

# Get complaint by id
def get_complaint_service(c_id):
    try:
        complaint = Complaint.query.get(c_id)
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        # Return your existing response
        return make_response(jsonify({'complaint' : complaint.json()}), 200)
    except Exception as e:
        return make_response(jsonify({'message' : "error getting complaint", 'error' : str(e)}), 500)

# Upvote a complaint
def upvote_complaint_service(c_id):
    try:
        data = request.get_json()
        user_id = data['user_id']
        
        # Get the complaint with for update lock to avoid race conditions
        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        # Initialize upvotes array if it's None
        if complaint.upvotes is None:
            complaint.upvotes = []
        
        # Convert user_id to int to ensure proper comparison
        user_id = int(user_id)
        
        # Check if user already upvoted
        if user_id not in complaint.upvotes:
            # Create a new list with the user_id added
            new_upvotes = complaint.upvotes.copy() if complaint.upvotes else []
            new_upvotes.append(user_id)
            
            # Update the upvotes field
            complaint.upvotes = new_upvotes
            
            # Commit the changes
            db.session.commit()
            
            print(f"Updated upvotes for complaint {c_id}: {complaint.upvotes}")
            
        return jsonify({
            'c_id': complaint.c_id,
            'user_id': complaint.user_id,
            'message': complaint.c_message,
            'upvotes': complaint.upvotes,
            'upvote_count': len(complaint.upvotes) if complaint.upvotes else 0
        }), 200
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in upvote_complaint: {str(e)}")
        return make_response(jsonify({'message': "error upvoting complaint", 'error': str(e)}), 500)

# decrease upvote a complaint
def downvote_complaint_service(c_id):
    try:
        data = request.get_json()
        user_id = data['user_id']
        
        # Get the complaint with for update lock to avoid race conditions
        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        # Initialize upvotes array if it's None
        if complaint.upvotes is None:
            complaint.upvotes = []
        
        # Convert user_id to int to ensure proper comparison
        user_id = int(user_id)
        
        # Check if user already upvoted
        if user_id in complaint.upvotes:
            # Create a new list with the user_id added
            new_upvotes = complaint.upvotes.copy() if complaint.upvotes else []
            new_upvotes.remove(user_id)
            
            # Update the upvotes field
            complaint.upvotes = new_upvotes
            
            # Commit the changes
            db.session.commit()
            
            print(f"Updated upvotes for complaint {c_id}: {complaint.upvotes}")
            
        return jsonify({
            'c_id': complaint.c_id,
            'user_id': complaint.user_id,
            'message': complaint.c_message,
            'upvotes': complaint.upvotes,
            'upvote_count': len(complaint.upvotes) if complaint.upvotes else 0
        }), 200
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in downvote_complaint: {str(e)}")
        return make_response(jsonify({'message': "error downvoting complaint", 'error': str(e)}), 500)

# Get number of upvotes for a complaint
def get_upvotes_service(c_id):
    try:
        # Get the complaint with for update lock to avoid race conditions
        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        return jsonify({
            'upvotes': len(complaint.upvotes) if complaint.upvotes else 0
        }), 200
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in get_upvotes: {str(e)}")
        return make_response(jsonify({'message': "error getting upvotes", 'error': str(e)}), 500)

# Add a resolver to a complaint
def add_resolver_service(c_id):
    try:
        data = request.get_json()
        user_id = data['user_id']

        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        # Initialize resolver array if it's None
        if complaint.resolver is None:
            complaint.resolver = []
        
        user_id = int(user_id)
        
        if user_id not in complaint.resolver:
            # Create a new list with the resolver_id added
            new_resolver = complaint.resolver.copy() if complaint.resolver else []
            new_resolver.append(user_id)
            complaint.resolver = new_resolver
            db.session.commit()
            
            print(f"Updated resolvers for complaint {c_id}: {complaint.resolver}")
            
        return jsonify({
            'c_id': complaint.c_id,
            'user_id': complaint.user_id,
            'message': complaint.c_message,
            'resolver': complaint.resolver,
            'resolver_count': len(complaint.resolver) if complaint.resolver else 0
        }), 200
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in add_resolver: {str(e)}")
        return make_response(jsonify({'message': "error adding resolver", 'error': str(e)}), 500) 

# Add Comment to a complaint
def add_comment_service(c_id):
    try:
        data = request.get_json()
        user_id = data['user_id']
        comment_message = data['comment']
        
        # Get the complaint with for update lock to avoid race conditions
        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        # Create a new comment
        new_comment = Comment(user_id = user_id, c_id=c_id, comment_message=comment_message)
        db.session.add(new_comment)
        
        # Commit the changes
        db.session.commit()
        
        return jsonify({
            'user_id': new_comment.user_id,
            'comment_id': new_comment.comment_id,
            'c_id': new_comment.c_id,
            'comment': new_comment.comment_message
        }), 201
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in add_comment: {str(e)}")
        return make_response(jsonify({'message': "error adding comment", 'error': str(e)}), 500)


# Get all comments for a complaint
def get_comments_service(c_id):
    try:
        # Get the complaint with for update lock to avoid race conditions
        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)
        
        comments = Comment.query.filter_by(c_id=c_id).all()
        
        if not comments:
            return make_response(jsonify({'comments': []}), 200)
        
        return jsonify({    
            'comments': [comment.json() for comment in comments]    
        }), 200
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in get_comments: {str(e)}")
        return make_response(jsonify({'message': "error getting comments", 'error': str(e)}), 500)

# Delete a comment from a complaint
def delete_comment_service(c_id, comment_id):
    try:
        # Get the complaint with for update lock to avoid race conditions
        complaint = Complaint.query.filter_by(c_id=c_id).first()
        
        if not complaint:
            return make_response(jsonify({'message': 'Complaint not found'}), 404)        
        
        comment = Comment.query.filter_by(comment_id=comment_id, c_id=c_id).first()
        
        if not comment:
            return make_response(jsonify({'message': 'Comment not found'}), 404)        
        
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({
            'comment_id': comment.comment_id,
            'c_id': comment.c_id,
            'c_message': comment.c_message
        }), 200
        
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        print(f"Error in delete_comment: {str(e)}")
        return make_response(jsonify({'message': "error deleting comment", 'error': str(e)}), 500)
    
# Delete a complaint
# Modify your delete_complaint_service function
def delete_complaint_service(c_id):
    try:
        complaint = Complaint.query.get(c_id)
        if not complaint:
            return jsonify({'error': 'Complaint not found'}), 404
        
        # Update stats before deleting
        stats = ComplaintStats.query.first()
        if not stats:
            # If no stats exist, create them based on the current state
            total_complaints = Complaint.query.count()
            stats = ComplaintStats(total_created=total_complaints + 1, total_resolved=1)
            db.session.add(stats)
        else:
            stats.total_resolved += 1
        
        # Delete the complaint
        db.session.delete(complaint)
        db.session.commit()
        
        return jsonify({'message': 'Complaint deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return jsonify({'error': str(e)}), 500

# Add this to your services.py file
def get_complaint_stats_service():
    try:
        # Get current active complaints (unresolved)
        active_complaints = Complaint.query.count()
        
        # Get the total complaints ever created from the ComplaintStats model
        stats = ComplaintStats.query.first()
        
        if not stats:
            # Initialize if no stats exist
            stats = ComplaintStats(total_created=active_complaints, total_resolved=0)
            db.session.add(stats)
            db.session.commit()
        
        # Calculate unresolved complaints as total created minus total resolved
        unresolved_complaints = stats.total_created - stats.total_resolved
        
        # If there's a discrepancy between active_complaints and calculated unresolved_complaints,
        # update the stats to reflect the actual state
        if active_complaints != unresolved_complaints:
            # This means our stats are out of sync, so we'll update them
            stats.total_created = active_complaints + stats.total_resolved
            db.session.commit()
            unresolved_complaints = active_complaints
        
        return jsonify({
            'total_complaints': stats.total_created,
            'resolved_complaints': stats.total_resolved,
            'unresolved_complaints': unresolved_complaints
        }), 200
    except Exception as e:
        db.session.rollback()  # Roll back in case of error
        return jsonify({'error': str(e)}), 500
    
