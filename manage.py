from dotenv import load_dotenv

load_dotenv()

from flask import url_for
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from model.db import db
from main import create_app

app = create_app()
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def delete_database(table):
    pass


if __name__ == '__main__':
    manager.run()
