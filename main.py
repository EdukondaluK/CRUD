import os
from flask import Flask
from flask_cors import CORS
from db.postgres import db
from controllers.location_controller import location_api
from controllers.department_controller import department_api
from controllers.category_controller import category_api
from controllers.sub_category_contoller import sub_category_api

app  = Flask(__name__,instance_relative_config=True)
cors = CORS(app,resources={"/*":{"origins": "*"}})
app.config['JSON_SORT_KEYS'] = False
db_string = ''

app.register_blueprint(location_api)
app.register_blueprint(department_api)
app.register_blueprint(category_api)
app.register_blueprint(sub_category_api)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    HTTP_PORT = 8080
    port = int(os.getenv('VCAP_APP_PORT', HTTP_PORT))
    environment = os.getenv('APPLICATION_ENV')
    db_type = os.getenv('APPLICATION_DB_TYPE')

    if environment is None:
        environment = 'default'

    if db_type is None:
        db_type = 'PG'

    print('-----------------------------------------------')
    print('Environment: ' + environment)
    print('Db Type: ' + db_type)
    print('-----------------------------------------------')

    config_file = 'config-' + environment

    app.config.from_object(config_file)

    # "postgres://username:password@hostname:port/database"
    db_string = 'postgres://' + app.config.get('DB_USERNAME') + ":" \
                + app.config.get('DB_PASSWORD') \
                + '@' + app.config.get('DB_HOST') \
                + ':' + app.config.get('DB_PORT') \
                + '/' + app.config.get('DB_DATABASE')

    # Set the environment variables to be used throughout the application.
    os.environ['DB_STRING'] = db_string
    app.config['SQLALCHEMY_DATABASE_URI'] = db_string

    db.init_app(app)
    app.run(host='localhost', port=port, threaded=True)
