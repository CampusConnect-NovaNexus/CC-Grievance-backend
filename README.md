# Grievance Management System API Documentation

This document provides details about the available API endpoints for the Grievance Management System. It is designed to help frontend developers integrate with the backend services.

## Base URL

All endpoints are prefixed with `/api/grievance`

## API Endpoints

### Test Server

**Endpoint:** `GET /test`

**Description:** Simple endpoint to check if the server is running.

**Response:**
```json
{
  "message": "Server is running"
}
```

### Create a Complaint

**Endpoint:** `POST /api/grievance/new_complaint`

**Description:** Creates a new complaint in the system.

**Request Body:**
```json
{
  "user_id": 123,
  "c_message": "This is my complaint message"
}
```

**Response:**
- **Status Code:** 201 (Created)
- **Body:**
```json
{
  "user_id": 123,
  "message": "This is my complaint message"
}
```

**Error Response:**
- **Status Code:** 500
- **Body:**
```json
{
  "message": "error creating complaint",
  "error": "Error details"
}
```

### Upvote a Complaint

**Endpoint:** `PUT /api/grievance/upvote/{c_id}`

**Description:** Adds a user's upvote to a specific complaint.

**URL Parameters:**
- `c_id`: ID of the complaint to upvote

**Request Body:**
```json
{
  "user_id": 123
}
```

**Response:**
- **Status Code:** 200 (OK)
- **Body:** Updated complaint data including upvotes

**Error Response:**
- **Status Code:** 404 if complaint not found
- **Status Code:** 500 for server errors

### Get Upvotes for a Complaint

**Endpoint:** `GET /api/grievance/get_upvotes/{c_id}`

**Description:** Retrieves the number of upvotes for a specific complaint.

**URL Parameters:**
- `c_id`: ID of the complaint

**Response:**
- **Status Code:** 200 (OK)
- **Body:** Contains upvote count and list of user IDs who upvoted

**Error Response:**
- **Status Code:** 404 if complaint not found
- **Status Code:** 500 for server errors

### Add Resolver to a Complaint

**Endpoint:** `PUT /api/grievance/add_resolver/{c_id}`

**Description:** Adds a user as a resolver for a specific complaint.

**URL Parameters:**
- `c_id`: ID of the complaint

**Request Body:**
```json
{
  "user_id": 123
}
```

**Response:**
- **Status Code:** 200 (OK)
- **Body:** Updated complaint data including resolvers

**Error Response:**
- **Status Code:** 404 if complaint not found
- **Status Code:** 500 for server errors

### Add Comment to a Complaint

**Endpoint:** `POST /api/grievance/add_comment/{c_id}`

**Description:** Adds a comment to a specific complaint.

**URL Parameters:**
- `c_id`: ID of the complaint to comment on

**Request Body:**
```json
{
  "user_id": 123,
  "c_message": "This is my comment"
}
```

**Response:**
- **Status Code:** 201 (Created)
- **Body:** Comment data including ID

**Error Response:**
- **Status Code:** 404 if complaint not found
- **Status Code:** 500 for server errors

### Get Comments for a Complaint

**Endpoint:** `GET /api/grievance/get_comments/{c_id}`

**Description:** Retrieves all comments for a specific complaint.

**URL Parameters:**
- `c_id`: ID of the complaint

**Response:**
- **Status Code:** 200 (OK)
- **Body:** Array of comment objects

**Error Response:**
- **Status Code:** 404 if complaint not found
- **Status Code:** 500 for server errors

### Delete a Comment

**Endpoint:** `DELETE /api/grievance/delete_comment/{c_id}/{comment_id}`

**Description:** Deletes a specific comment from a complaint.

**URL Parameters:**
- `c_id`: ID of the complaint
- `comment_id`: ID of the comment to delete

**Response:**
- **Status Code:** 200 (OK)
- **Body:** Success message

**Error Response:**
- **Status Code:** 404 if complaint or comment not found
- **Status Code:** 500 for server errors

### Delete a Complaint

**Endpoint:** `DELETE /api/grievance/delete_complaint/{c_id}`

**Description:** Deletes a specific complaint and all associated comments.

**URL Parameters:**
- `c_id`: ID of the complaint to delete

**Response:**
- **Status Code:** 200 (OK)
- **Body:** Success message

**Error Response:**
- **Status Code:** 404 if complaint not found
- **Status Code:** 500 for server errors

## Data Models

### Complaint

```json
{
  "c_id": 1,
  "user_id": 123,
  "c_message": "Complaint message",
  "upvotes": [122, 123, 124],
  "resolver": [125, 126]
}
```

### Comment

```json
{
  "comment_id": 1,
  "c_id": 1,
  "user_id": 123,
  "c_message": "Comment message"
}
```

## Additional Notes

1. All error responses include a message and details about the error.
2. The `user_id` is required for most operations to track who performed the action.
3. Upvotes and resolver lists prevent duplicate entries from the same user.
