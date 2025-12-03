# Week 16, Day 1: Building a Complete Blog Application with Flask

## Session Overview
Today's session focused on building a production-ready blog application from scratch using Flask, SQLAlchemy, and MySQL. We covered proper project structure, database relationships, and modern best practices.

## Key Topics Covered

### 1. **Project Setup & Environment**
- Created a new Flask project with proper virtual environment setup
- Installed required packages:
  - Flask
  - Flask-SQLAlchemy (for easier database integration)
  - PyMySQL (for MySQL connectivity)
  - Bcrypt (for password hashing)
  - PyJWT (for authentication tokens)

### 2. **Database Configuration**
- **Switched from SQLite to MySQL** - a more robust, production-ready database
- Created MySQL database: `flask_blog_app`
- Configured connection string: `mysql+pymysql://username:password@localhost/database_name`
- Used Flask's `app.config['SQLALCHEMY_DATABASE_URI']` for database connection

### 3. **Database Models & Relationships**

#### **Three Main Tables Created:**

**Users Table:**
- `id` (primary key)
- `email` (unique)
- `password_hash`
- `role` (user/admin)
- `created_at`, `updated_at` (automatic timestamps)

**Posts Table:**
- `id` (primary key)
- `title`
- `content` (using TEXT datatype for large content)
- `user_id` (foreign key to Users)
- `created_at`, `updated_at`

**Tags Table:**
- `id` (primary key)
- `name`
- `created_at`, `updated_at`

**Post_Tags Table (Junction Table):**
- `post_id` (foreign key to Posts)
- `tag_id` (foreign key to Tags)
- Enables many-to-many relationship

#### **Relationship Types:**
- **One-to-Many**: Users → Posts (one user can have many posts)
- **Many-to-Many**: Posts ↔ Tags (posts can have multiple tags, tags can belong to multiple posts)

### 4. **Important SQLAlchemy Concepts**

**Key Differences with Flask-SQLAlchemy:**
- Models inherit from `db.Model` instead of `Base`
- Use `db.Column()` and `mapped_column()`
- Access queries via `Model.query.filter()` or `Model.query.filter_by()`

**String vs Text:**
- Use `String(255)` for shorter fields (titles, names, emails)
- Use `Text` for longer content where length is unknown
- MySQL requires explicit string lengths

**Timestamps:**
- Use `server_default=func.now()` for `created_at`
- Add `onupdate=func.now()` for `updated_at`

**Foreign Keys:**
- Must explicitly define using `db.ForeignKey('table_name.column_name')`
- Use `db.relationship()` with `back_populates` to enable object access

### 5. **Query Methods: filter() vs filter_by()**

**filter_by():**
```python
User.query.filter_by(email=email).first()
```
- Simple equality checks only
- Uses keyword arguments

**filter():**
```python
Tag.query.filter(Tag.id.in_(tag_ids)).all()
```
- Supports complex expressions
- Required for operations like `.in_()`, comparisons, etc.
- Access columns via `Model.column_name`

### 6. **CRUD Operations Built**

**Authentication Routes:**
- `/register` - Create new user with hashed password
- `/login` - Authenticate user and return JWT token

**Posts Routes:**
- `POST /posts` - Create new post with associated tags
- `GET /posts` - Retrieve all posts
- `GET /posts/<id>` - Get single post
- `PUT /posts/<id>` - Update post
- `DELETE /posts/<id>` - Delete post

**Tags Routes:**
- Similar CRUD operations for managing tags

### 7. **JWT Authentication**
- Created `create_access_token()` function
- Token includes:
  - `sub`: User ID (as string)
  - `exp`: Expiration time (30 minutes)
  - `iat`: Issued at timestamp
- Used HS256 algorithm
- Secret key stored in `app.config['JWT_SECRET_KEY']`

### 8. **Code Organization with Blueprints**

**Why Blueprints?**
- Avoid putting all routes in one file
- Group related functionality together
- Make code more maintainable and scalable

**Blueprint Structure Created:**
```
routes/
├── __init__.py
├── posts.py (posts_bp)
├── tags.py (tags_bp)
└── auth.py (auth_bp)

utilities/
├── __init__.py
└── jwt.py
```

**Blueprint Implementation:**
```python
# In routes/posts.py
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['POST'])
def create_post():
    # Route logic

# In app.py
app.register_blueprint(posts_bp, url_prefix='/posts')
```

**URL Prefixes:**
- Add `url_prefix` when registering blueprints
- All routes in that blueprint automatically get the prefix
- Example: `url_prefix='/posts'` makes all routes start with `/posts`

### 9. **Important Python Concepts**

**Modules:**
- Create `__init__.py` to mark a folder as a Python module
- Enables importing from that folder

**Circular Imports:**
- Encountered when files import each other
- **Solution**: Use Flask's `current_app` instead of importing `app`
```python
from flask import current_app
# Access config: current_app.config['KEY']
```

**List Comprehensions for Data Formatting:**
```python
tags = [{'id': tag.id, 'name': tag.name} for tag in post.tags]
```

### 10. **Handling Many-to-Many Relationships**

**Creating Posts with Tags:**
1. Receive tag IDs from frontend: `[1, 2, 3]`
2. Query database to get tag objects:
   ```python
   tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
   ```
3. Create post with tag objects:
   ```python
   post = Post(title=title, content=content, tags=tags)
   ```

**Key Point:** ORMs work with objects, not IDs. You must convert IDs to objects before assigning relationships.

### 11. **Data Types & Validation**

**String Length:**
- Python's `len()` function gets list/string length
- Not `.count()` (that's for counting occurrences)

**Nullable Fields:**
- Use `nullable=False` to require values
- Empty strings can still bypass this (need additional validation)

**Unique Constraints:**
- Add `unique=True` to prevent duplicates at database level

## Best Practices Highlighted

1. **Always validate user input** before database operations
2. **Hash passwords** - never store plain text
3. **Use foreign keys** to maintain data integrity
4. **Separate concerns** using blueprints
5. **Use TEXT datatype** for variable-length content
6. **Add timestamps** to track record changes
7. **Provide meaningful error messages** without exposing security details
8. **Use utility functions** for reusable code (like JWT creation)

## Common Mistakes to Avoid

1. Using `filter_by()` with expressions like `.in_()` (use `filter()` instead)
2. Forgetting to convert tag IDs to tag objects for relationships
3. Creating circular imports between files
4. Not using `.all()` vs `.first()` appropriately
5. Forgetting semicolons in MySQL command line

## Next Steps

- Implement login-required decorators to protect routes
- Create the React frontend to consume these APIs
- Add more advanced features as needed

## Key Takeaway

This session demonstrated how to build a **complete, well-structured Flask application** with proper:
- Database design (one-to-many and many-to-many relationships)
- Code organization (blueprints and utilities)
- Authentication (JWT tokens)
- CRUD operations for all resources
- Modern SQLAlchemy practices

**Remember:** Review the code thoroughly, understand each part, and ask questions before the next session. We'll be building on this foundation!# Week 16, Day 1: Building a Complete Blog Application with Flask

## Session Overview
Today's session focused on building a production-ready blog application from scratch using Flask, SQLAlchemy, and MySQL. We covered proper project structure, database relationships, and modern best practices.

## Key Topics Covered

### 1. **Project Setup & Environment**
- Created a new Flask project with proper virtual environment setup
- Installed required packages:
  - Flask
  - Flask-SQLAlchemy (for easier database integration)
  - PyMySQL (for MySQL connectivity)
  - Bcrypt (for password hashing)
  - PyJWT (for authentication tokens)

### 2. **Database Configuration**
- **Switched from SQLite to MySQL** - a more robust, production-ready database
- Created MySQL database: `flask_blog_app`
- Configured connection string: `mysql+pymysql://username:password@localhost/database_name`
- Used Flask's `app.config['SQLALCHEMY_DATABASE_URI']` for database connection

### 3. **Database Models & Relationships**

#### **Three Main Tables Created:**

**Users Table:**
- `id` (primary key)
- `email` (unique)
- `password_hash`
- `role` (user/admin)
- `created_at`, `updated_at` (automatic timestamps)

**Posts Table:**
- `id` (primary key)
- `title`
- `content` (using TEXT datatype for large content)
- `user_id` (foreign key to Users)
- `created_at`, `updated_at`

**Tags Table:**
- `id` (primary key)
- `name`
- `created_at`, `updated_at`

**Post_Tags Table (Junction Table):**
- `post_id` (foreign key to Posts)
- `tag_id` (foreign key to Tags)
- Enables many-to-many relationship

#### **Relationship Types:**
- **One-to-Many**: Users → Posts (one user can have many posts)
- **Many-to-Many**: Posts ↔ Tags (posts can have multiple tags, tags can belong to multiple posts)

### 4. **Important SQLAlchemy Concepts**

**Key Differences with Flask-SQLAlchemy:**
- Models inherit from `db.Model` instead of `Base`
- Use `db.Column()` and `mapped_column()`
- Access queries via `Model.query.filter()` or `Model.query.filter_by()`

**String vs Text:**
- Use `String(255)` for shorter fields (titles, names, emails)
- Use `Text` for longer content where length is unknown
- MySQL requires explicit string lengths

**Timestamps:**
- Use `server_default=func.now()` for `created_at`
- Add `onupdate=func.now()` for `updated_at`

**Foreign Keys:**
- Must explicitly define using `db.ForeignKey('table_name.column_name')`
- Use `db.relationship()` with `back_populates` to enable object access

### 5. **Query Methods: filter() vs filter_by()**

**filter_by():**
```python
User.query.filter_by(email=email).first()
```
- Simple equality checks only
- Uses keyword arguments

**filter():**
```python
Tag.query.filter(Tag.id.in_(tag_ids)).all()
```
- Supports complex expressions
- Required for operations like `.in_()`, comparisons, etc.
- Access columns via `Model.column_name`

### 6. **CRUD Operations Built**

**Authentication Routes:**
- `/register` - Create new user with hashed password
- `/login` - Authenticate user and return JWT token

**Posts Routes:**
- `POST /posts` - Create new post with associated tags
- `GET /posts` - Retrieve all posts
- `GET /posts/<id>` - Get single post
- `PUT /posts/<id>` - Update post
- `DELETE /posts/<id>` - Delete post

**Tags Routes:**
- Similar CRUD operations for managing tags

### 7. **JWT Authentication**
- Created `create_access_token()` function
- Token includes:
  - `sub`: User ID (as string)
  - `exp`: Expiration time (30 minutes)
  - `iat`: Issued at timestamp
- Used HS256 algorithm
- Secret key stored in `app.config['JWT_SECRET_KEY']`

### 8. **Code Organization with Blueprints**

**Why Blueprints?**
- Avoid putting all routes in one file
- Group related functionality together
- Make code more maintainable and scalable

**Blueprint Structure Created:**
```
routes/
├── __init__.py
├── posts.py (posts_bp)
├── tags.py (tags_bp)
└── auth.py (auth_bp)

utilities/
├── __init__.py
└── jwt.py
```

**Blueprint Implementation:**
```python
# In routes/posts.py
posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/', methods=['POST'])
def create_post():
    # Route logic

# In app.py
app.register_blueprint(posts_bp, url_prefix='/posts')
```

**URL Prefixes:**
- Add `url_prefix` when registering blueprints
- All routes in that blueprint automatically get the prefix
- Example: `url_prefix='/posts'` makes all routes start with `/posts`

### 9. **Important Python Concepts**

**Modules:**
- Create `__init__.py` to mark a folder as a Python module
- Enables importing from that folder

**Circular Imports:**
- Encountered when files import each other
- **Solution**: Use Flask's `current_app` instead of importing `app`
```python
from flask import current_app
# Access config: current_app.config['KEY']
```

**List Comprehensions for Data Formatting:**
```python
tags = [{'id': tag.id, 'name': tag.name} for tag in post.tags]
```

### 10. **Handling Many-to-Many Relationships**

**Creating Posts with Tags:**
1. Receive tag IDs from frontend: `[1, 2, 3]`
2. Query database to get tag objects:
   ```python
   tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
   ```
3. Create post with tag objects:
   ```python
   post = Post(title=title, content=content, tags=tags)
   ```

**Key Point:** ORMs work with objects, not IDs. You must convert IDs to objects before assigning relationships.

### 11. **Data Types & Validation**

**String Length:**
- Python's `len()` function gets list/string length
- Not `.count()` (that's for counting occurrences)

**Nullable Fields:**
- Use `nullable=False` to require values
- Empty strings can still bypass this (need additional validation)

**Unique Constraints:**
- Add `unique=True` to prevent duplicates at database level

## Best Practices Highlighted

1. **Always validate user input** before database operations
2. **Hash passwords** - never store plain text
3. **Use foreign keys** to maintain data integrity
4. **Separate concerns** using blueprints
5. **Use TEXT datatype** for variable-length content
6. **Add timestamps** to track record changes
7. **Provide meaningful error messages** without exposing security details
8. **Use utility functions** for reusable code (like JWT creation)

## Common Mistakes to Avoid

1. Using `filter_by()` with expressions like `.in_()` (use `filter()` instead)
2. Forgetting to convert tag IDs to tag objects for relationships
3. Creating circular imports between files
4. Not using `.all()` vs `.first()` appropriately
5. Forgetting semicolons in MySQL command line

## Next Steps

- Implement login-required decorators to protect routes
- Create the React frontend to consume these APIs
- Add more advanced features as needed

## Key Takeaway

This session demonstrated how to build a **complete, well-structured Flask application** with proper:
- Database design (one-to-many and many-to-many relationships)
- Code organization (blueprints and utilities)
- Authentication (JWT tokens)
- CRUD operations for all resources
- Modern SQLAlchemy practices

**Remember:** Review the code thoroughly, understand each part, and ask questions before the next session. We'll be building on this foundation!