from datetime import datetime
from app import app, db
from models import User, Article, Tag, ArticleTag
from slugify import slugify
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def seed_database():
    with app.app_context():
        # Clear existing data
        ArticleTag.query.delete()
        Article.query.delete()
        Tag.query.delete()
        User.query.delete()
        
        print("Creating users...")
        users = [
            User(
                email="john@example.com",
                password_hash=hash_password("password123"),
                name="John Doe",
                role="user"
            ),
            User(
                email="jane@example.com",
                password_hash=hash_password("password123"),
                name="Jane Smith",
                role="user"
            )
        ]
        db.session.add_all(users)
        db.session.flush()
        
        print("Creating tags...")
        tags = [
            Tag(title="Python", slug=slugify("Python")),
            Tag(title="JavaScript", slug=slugify("JavaScript")),
            Tag(title="React", slug=slugify("React")),
            Tag(title="Backend", slug=slugify("Backend")),
            Tag(title="Frontend", slug=slugify("Frontend")),
            Tag(title="Web Development", slug=slugify("Web Development")),
        ]
        db.session.add_all(tags)
        db.session.flush()
        
        print("Creating articles...")
        articles = [
            Article(
                title="Getting Started with Python",
                slug=slugify("Getting Started with Python"),
                excerpt="Learn the basics of Python programming language",
                featured_image_url="https://placehold.co/800x400?text=Python&bg=3776AB&fg=FFFFFF",
                read_time_minutes=5,
                status="published",
                content="Python is a versatile and beginner-friendly programming language. In this article, we'll explore the fundamentals of Python and get you started on your programming journey.",
                author_id=users[0].id,
                published_at=datetime.now()
            ),
            Article(
                title="Building React Components",
                slug=slugify("Building React Components"),
                excerpt="Master the art of creating reusable React components",
                featured_image_url="https://placehold.co/800x400?text=React&bg=61DAFB&fg=000000",
                read_time_minutes=8,
                status="published",
                content="React components are the building blocks of modern web applications. Learn how to create functional and class-based components, manage state, and handle events effectively.",
                author_id=users[1].id,
                published_at=datetime.now()
            ),
            Article(
                title="RESTful API Design Best Practices",
                slug=slugify("RESTful API Design Best Practices"),
                excerpt="Design scalable and maintainable REST APIs",
                featured_image_url="https://placehold.co/800x400?text=API&bg=009688&fg=FFFFFF",
                read_time_minutes=10,
                status="published",
                content="Designing a good REST API is crucial for building scalable web applications. This article covers best practices including resource naming, HTTP methods, status codes, and versioning strategies.",
                author_id=users[0].id,
                published_at=datetime.now()
            ),
            Article(
                title="JavaScript ES6 Features",
                slug=slugify("JavaScript ES6 Features"),
                excerpt="Explore modern JavaScript features that improve code quality",
                featured_image_url="https://placehold.co/800x400?text=JavaScript&bg=F7DF1E&fg=000000",
                read_time_minutes=7,
                status="published",
                content="ES6 (ES2015) introduced many powerful features to JavaScript including arrow functions, classes, template literals, destructuring, and promises. Discover how these features can make your code more readable and efficient.",
                author_id=users[1].id,
                published_at=datetime.now()
            ),
            Article(
                title="Database Optimization Techniques",
                slug=slugify("Database Optimization Techniques"),
                excerpt="Tips for optimizing database queries and performance",
                featured_image_url="https://placehold.co/800x400?text=Database&bg=336791&fg=FFFFFF",
                read_time_minutes=12,
                status="published",
                content="Database performance is critical for application speed. Learn about indexing, query optimization, caching strategies, and database design patterns to improve your application's performance.",
                author_id=users[0].id,
                published_at=datetime.now()
            ),
            Article(
                title="Introduction to Flask Framework",
                slug=slugify("Introduction to Flask Framework"),
                excerpt="Build lightweight web applications with Flask",
                featured_image_url="https://placehold.co/800x400?text=Flask&bg=000000&fg=FFFFFF",
                read_time_minutes=6,
                status="published",
                content="Flask is a lightweight web framework for Python that makes it easy to build web applications. This guide covers the basics of routing, request handling, templates, and database integration.",
                author_id=users[1].id,
                published_at=datetime.now()
            ),
        ]
        db.session.add_all(articles)
        db.session.flush()
        
        print("Linking articles with tags...")
        # Link articles with tags
        article_tags_map = [
            (articles[0], [tags[0]]),  # Python
            (articles[1], [tags[1], tags[2], tags[4]]),  # JavaScript, React, Frontend
            (articles[2], [tags[3], tags[5]]),  # Backend, Web Development
            (articles[3], [tags[1]]),  # JavaScript
            (articles[4], [tags[3], tags[5]]),  # Backend, Web Development
            (articles[5], [tags[0], tags[3], tags[5]]),  # Python, Backend, Web Development
        ]
        
        for article, article_tags in article_tags_map:
            for tag in article_tags:
                article_tag = ArticleTag(article_id=article.id, tag_id=tag.id)
                db.session.add(article_tag)
        
        db.session.commit()
        print("✅ Database seeded successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(tags)} tags")
        print(f"Created {len(articles)} articles")

if __name__ == "__main__":
    seed_database()
