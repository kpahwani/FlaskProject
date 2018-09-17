"""
Doctsring
"""
from thermos.models import User, Bookmark, Tag
from flask_script import Manager, prompt_bool
from thermos.views import app, db
from flask_migrate import Migrate, MigrateCommand

MANAGER = Manager(app)
MIGRATE = Migrate(app, db)
MANAGER.add_command('db', MigrateCommand)


@MANAGER.command
def initdb():
    """
    Doctsring
    """
    db.create_all()
    print("Initialized the database")


@MANAGER.command
def dropdb():
    """
    Doctsring
    """
    if prompt_bool('Are you sure you want to drop the database'):
        db.drop_all()
        print("Dropped the database")


if __name__ == '__main__':
    MANAGER.run()
