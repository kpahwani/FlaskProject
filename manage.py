"""
Doctsring
"""
from flask_script import Manager, prompt_bool
from thermos.views import app, db

MANAGER = Manager(app)


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
