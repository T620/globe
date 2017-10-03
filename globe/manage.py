import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from globe import app, db


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
print db


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
