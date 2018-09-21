"""
Doctsring
"""
import os

from thermos import db, create_app

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('THERMOS_ENV') or 'dev')
MANAGER = Manager(app)

MIGRATE = Migrate(app, db)
MANAGER.add_command('db', MigrateCommand)


if __name__ == '__main__':
    MANAGER.run()
