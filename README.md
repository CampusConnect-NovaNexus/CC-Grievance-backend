# Grievance System API Documentation

This document provides detailed information about the API endpoints available in the Campus Connect Grievance System backend.

## Base URL

All API endpoints are prefixed with `/api/grievance`.

## Standard Endpoints

### Test Connection
- **Endpoint**: `/test`
- **Method**: `GET`
- **Description**: Simple endpoint to check if the server is running.
- **Response**:
  ```json
  {
    "message": "Server is running"
  }
  ```

### Get Complaint Statistics
- **Endpoint**: `/api/grievance/stats`
- **Method**: `GET`
- **Description**: Retrieves statistics about complaints in the system.
- **Response**:
  ```json
  {
    "total_complaints": 100,
    "resolved_complaints": 75,
    "unresolved_complaints": 25
  }
  ```

### Create a New Complaint
- **Endpoint**: `/api/grievance/new_complaint`
- **Method**: `POST`
- **Description**: Creates a new complaint in the system.
- **Request Body (JSON)**:
  ```json
  {
    "user_id": "user123",
    "complaint_title": "Issue with Campus WiFi",
    "complaint_message": "The WiFi in the library has been down for two days.",
    "category": "Infrastructure"
  }
  ```
- **Request Body (Multipart Form Data)**:
  - `user_id`: ID of the user creating the complaint
  - `title`: Title of the complaint
  - `description`: Detailed description of the complaint
  - `category`: Category of the complaint (optional, defaults to "Others")
  - `image_file`: Image file related to the complaint (optional)
- **Response**:
  ```json
  {
    "c_id": "uuid-string",
    "user_id": "user123",
    "title": "Issue with Campus WiFi",
    "description": "The WiFi in the library has been down for two days.",
    "upvotes": [],
    "resolver": [],
    "created_at": "2023-06-15T14:30:00Z",
    "category": "Infrastructure"
  }
  ```

### Get All Complaints
- **Endpoint**: `/api/grievance/complaints`
- **Method**: `GET`
- **Description**: Retrieves all complaints in the system.
- **Response**:
  ```json
  {
    "complaints": [
      {
        "c_id": "uuid-string",
        "user_id": "user123",
        "title": "Issue with Campus WiFi",
        "description": "The WiFi in the library has been down for two days.",
        "upvotes": [1, 2, 3],
        "resolver": [4],
        "created_at": "2023-06-15T14:30:00Z",
        "category": "Infrastructure",
        "comment_count": 5
      },
      // More complaints...
    ]
  }
  ```

### Get Complaint by ID
- **Endpoint**: `/api/grievance/complaint/<c_id>`
- **Method**: `GET`
- **Description**: Retrieves a specific complaint by its ID.
- **URL Parameters**:
  - `c_id`: The ID of the complaint to retrieve.
- **Response**:
  ```json
  {
    "complaint": {
      "c_id": "uuid-string",
      "user_id": "user123",
      "title": "Issue with Campus WiFi",
      "description": "The WiFi in the library has been down for two days.",
      "upvotes": [1, 2, 3],
      "resolver": [4],
      "created_at": "2023-06-15T14:30:00Z",
      "category": "Infrastructure"
    }
  }
  ```

### Get Complaint by User ID
- **Endpoint**: `/api/grievance/user/<user_id>`
- **Method**: `GET`
- **Description**: Retrieves complaints for a specific user.
- **URL Parameters**:
  - `user_id`: The ID of the user.
- **Response**:
  ```json
  {
    "complaint": {
      "c_id": "uuid-string",
      "user_id": "user123",
      "title": "Issue with Campus WiFi",
      "description": "The WiFi in the library has been down for two days.",
      "upvotes": [1, 2, 3],
      "resolver": [4],
      "created_at": "2023-06-15T14:30:00Z",
      "category": "Infrastructure"
    }
  }
  ```

### Upvote a Complaint
- **Endpoint**: `/api/grievance/upvote/<c_id>`
- **Method**: `PUT`
- **Description**: Adds an upvote to a complaint from a specific user.
- **URL Parameters**:
  - `c_id`: The ID of the complaint to upvote.
- **Request Body**:
  ```json
  {
    "user_id": "user456"
  }
  ```
- **Response**:
  ```json
  {
    "c_id": "uuid-string",
    "user_id": "user123",
    "title": "Issue with Campus WiFi",
    "description": "The WiFi in the library has been down for two days.",
    "upvotes": [1, 2, 3, 456],
    "upvote_count": 4
  }
  ```

### Downvote a Complaint
- **Endpoint**: `/api/grievance/downvote/<c_id>`
- **Method**: `PUT`
- **Description**: Removes an upvote from a complaint for a specific user.
- **URL Parameters**:
  - `c_id`: The ID of the complaint to downvote.
- **Request Body**:
  ```json
  {
    "user_id": "user456"
  }
  ```
- **Response**:
  ```json
  {
    "c_id": "uuid-string",
    "user_id": "user123",
    "title": "Issue with Campus WiFi",
    "description": "The WiFi in the library has been down for two days.",
    "upvotes": [1, 2, 3],
    "upvote_count": 3
  }
  ```

### Get Upvotes for a Complaint
- **Endpoint**: `/api/grievance/get_upvotes/<c_id>`
- **Method**: `GET`
- **Description**: Gets the number of upvotes for a specific complaint.
- **URL Parameters**:
  - `c_id`: The ID of the complaint.
- **Response**:
  ```json
  {
    "upvotes": 3
  }
  ```

### Add a Resolver to a Complaint
- **Endpoint**: `/api/grievance/add_resolver/<c_id>`
- **Method**: `PUT`
- **Description**: Adds a user as a resolver for a specific complaint.
- **URL Parameters**:
  - `c_id`: The ID of the complaint.
- **Request Body**:
  ```json
  {
    "user_id": "admin789"
  }
  ```
- **Response**:
  ```json
  {
    "c_id": "uuid-string",
    "user_id": "user123",
    "message": "The WiFi in the library has been down for two days.",
    "resolver": [789],
    "resolver_count": 1
  }
  ```

### Add a Comment to a Complaint
- **Endpoint**: `/api/grievance/add_comment/<c_id>`
- **Method**: `POST`
- **Description**: Adds a comment to a specific complaint.
- **URL Parameters**:
  - `c_id`: The ID of the complaint.
- **Request Body**:
  ```json
  {
    "user_id": "user456",
    "comment": "I'm experiencing the same issue."
  }
  ```
- **Response**:
  ```json
  {
    "user_id": "user456",
    "comment_id": "comment-uuid",
    "c_id": "complaint-uuid",
    "comment": "I'm experiencing the same issue."
  }
  ```

### Get Comments for a Complaint
- **Endpoint**: `/api/grievance/get_comments/<c_id>`
- **Method**: `GET`
- **Description**: Retrieves all comments for a specific complaint.
- **URL Parameters**:
  - `c_id`: The ID of the complaint.
- **Response**:
  ```json
  {
    "comments": [
      {
        "comment_id": "comment-uuid-1",
        "c_id": "complaint-uuid",
        "c_message": "I'm experiencing the same issue.",
        "created_at": "2023-06-15T15:30:00Z"
      },
      // More comments...
    ]
  }
  ```

### Delete a Comment
- **Endpoint**: `/api/grievance/delete_comment/<c_id>/<comment_id>`
- **Method**: `DELETE`
- **Description**: Deletes a specific comment from a complaint.
- **URL Parameters**:
  - `c_id`: The ID of the complaint.
  - `comment_id`: The ID of the comment to delete.
- **Response**:
  ```json
  {
    "comment_id": "comment-uuid",
    "c_id": "complaint-uuid",
    "c_message": "I'm experiencing the same issue."
  }
  ```

### Delete a Complaint
- **Endpoint**: `/api/grievance/delete_complaint/<c_id>`
- **Method**: `DELETE`
- **Description**: Deletes a specific complaint and all its associated comments.
- **URL Parameters**:
  - `c_id`: The ID of the complaint to delete.
- **Response**:
  ```json
  {
    "message": "Complaint deleted successfully"
  }
  ```

## AI-Related Endpoints

### Embed and Store Complaint
- **Endpoint**: `/api/grievance/ai/embed_store`
- **Method**: `POST`
- **Description**: Creates vector embeddings for a complaint and stores them in the vector database for similarity search.
- **Request Body**:
  ```json
  {
    "c_id": "complaint-uuid",
    "c_message": "The WiFi in the library has been down for two days."
  }
  ```
- **Response**:
  ```json
  {
    "message": "Successfully inserted vectors"
  }
  ```

### Query Similar Complaints
- **Endpoint**: `/api/grievance/ai/query`
- **Method**: `POST`
- **Description**: Searches for complaints similar to the provided text using vector similarity.
- **Request Body**:
  ```json
  {
    "c_message": "WiFi not working in the library"
  }
  ```
- **Response**:
  ```json
  {
    "similar_complaints": [
      {
        "c_id": "complaint-uuid-1",
        "content_preview": "The WiFi in the library has been down for two days..."
      },
      {
        "c_id": "complaint-uuid-2",
        "content_preview": "Internet connection issues in the campus library..."
      },
      // More similar complaints...
    ]
  }
  ```

## Error Responses

All endpoints may return the following error responses:

- **400 Bad Request**:
  ```json
  {
    "message": "Missing required fields"
  }
  ```

- **404 Not Found**:
  ```json
  {
    "message": "Complaint not found"
  }
  ```

- **500 Internal Server Error**:
  ```json
  {
    "message": "error [operation] complaint",
    "error": "Error message details"
  }
  ```

## Data Models

### Complaint
- `c_id`: Unique identifier for the complaint (UUID)
- `user_id`: ID of the user who created the complaint
- `complaint_title`: Title of the complaint (max 30 characters)
- `complaint_message`: Content of the complaint (max 120 characters)
- `upvotes`: Array of user IDs who upvoted the complaint
- `resolver`: Array of user IDs who are resolving the complaint
- `created_at`: Timestamp when the complaint was created
- `complaint_image_url`: URL to an image related to the complaint (optional)
- `complaint_category`: Category of the complaint (defaults to "Others")

### Comment
- `comment_id`: Unique identifier for the comment (UUID)
- `c_id`: ID of the complaint this comment belongs to
- `user_id`: ID of the user who created the comment
- `comment_message`: Content of the comment (max 120 characters)
- `created_at`: Timestamp when the comment was created

### ComplaintStats
- `total_created`: Total number of complaints ever created
- `total_resolved`: Total number of complaints that have been resolved