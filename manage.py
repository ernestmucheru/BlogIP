import os
from app import create_app,db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, migrate


app = create_app(os.getenv('FLASK_CONFIG')or 'default')
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()
