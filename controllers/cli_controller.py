from flask import Blueprint
from init import db, bcrypt
from datetime import date
from models.card import Card
from models.user import User
from models.comment import Comment


db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('eggs').decode('utf-8'),
            is_admin=True
        ),
        User(
            name='John Cleese',
            email='someone@spam.com',
            password=bcrypt.generate_password_hash('12345').decode('utf-8')
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    cards = [
        Card(
            title = 'Start the project',
            description = 'Stage 1 - Create the database',
            status = 'To Do',
            priority = 'High',
            date = date.today(),
            user = users[0]
        ),
        Card(
            title = "SQLAlchemy",
            description = "Stage 2 - Integrate ORM",
            status = "Ongoing",
            priority = "High",
            date = date.today(),
            user = users[0]
        ),
        Card(
            title = "ORM Queries",
            description = "Stage 3 - Implement several queries",
            status = "Ongoing",
            priority = "Medium",
            date = date.today(),
            user = users[1]
        ),
        Card(
            title = "Marshmallow",
            description = "Stage 4 - Implement Marshmallow to jsonify models",
            status = "Ongoing",
            priority = "Medium",
            date = date.today(),
            user = users[1]
        )
    ]

    db.session.add_all(cards)
    db.session.commit()

    comments = [
        Comment(
            message = 'Comment 1',
            user = users[1],
            card = cards[0],
            date = date.today()
        ),
        Comment(
            message = 'Comment 2',
            user = users[0],
            card = cards[0],
            date = date.today()
        ),
        Comment(
            message = 'Comment 3',
            user = users[0],
            card = cards[2],
            date = date.today()
        )
    ]

    db.session.add_all(comments)
    db.session.commit()

    print('Tables seeded')