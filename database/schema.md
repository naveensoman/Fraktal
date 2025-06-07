# Database Schema

This document defines the schema for the project's database.

## `users` Table

Stores information about registered users.

| Column        | Data Type     | Constraints        | Description                                   |
|---------------|---------------|--------------------|-----------------------------------------------|
| `user_id`     | INT           | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the user.             |
| `username`    | VARCHAR(255)  | UNIQUE, NOT NULL   | User's chosen username.                       |
| `password_hash`| VARCHAR(255)  | NOT NULL           | Hashed password for user authentication.      |
| `email`       | VARCHAR(255)  | UNIQUE, NOT NULL   | User's email address.                         |
| `created_at`  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP | Timestamp of when the user account was created. |

## `posts` Table

Stores blog posts created by users.

| Column        | Data Type     | Constraints        | Description                                   |
|---------------|---------------|--------------------|-----------------------------------------------|
| `post_id`     | INT           | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the post.             |
| `user_id`     | INT           | NOT NULL, FOREIGN KEY (users.user_id) | ID of the user who created the post.         |
| `title`       | VARCHAR(255)  | NOT NULL           | Title of the blog post.                       |
| `content`     | TEXT          | NOT NULL           | Main content of the blog post.                |
| `created_at`  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP | Timestamp of when the post was created.       |
| `updated_at`  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | Timestamp of when the post was last updated. |

## `comments` Table

Stores comments made by users on blog posts.

| Column        | Data Type     | Constraints        | Description                                   |
|---------------|---------------|--------------------|-----------------------------------------------|
| `comment_id`  | INT           | PRIMARY KEY, AUTO_INCREMENT | Unique identifier for the comment.          |
| `post_id`     | INT           | NOT NULL, FOREIGN KEY (posts.post_id) | ID of the post the comment belongs to.      |
| `user_id`     | INT           | NOT NULL, FOREIGN KEY (users.user_id) | ID of the user who wrote the comment.       |
| `content`     | TEXT          | NOT NULL           | The content of the comment.                   |
| `created_at`  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP | Timestamp of when the comment was created.    |
