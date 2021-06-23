import os
from app import create_app,db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand, migrate
from app.models import User, Post

app = create_app('production')

app = create_app(os.getenv('FLASK_CONFIG')or 'default')
manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.shell
def make_shell_context():
    return dict(app = app,db = db,User = User, Post=Post)

if __name__ == '__main__':
    manager.run()
