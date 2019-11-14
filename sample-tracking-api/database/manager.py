from app import app
from database.models import db
from flask_migrate import Migrate , MigrateCommand
from flask_script import Manager

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)