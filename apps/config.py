import os

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    # SECRET_KEY = config('SECRET_KEY'  , default='S#perS3crEt_007')
    SECRET_KEY = os.getenv('SECRET_KEY', 'S#perS3crEt_007')

    # This will create a file in <app> FOLDER
    # MySQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        os.getenv('DB_ENGINE'   , 'mysql'),
        os.getenv('DB_USERNAME' , 'root'),
        os.getenv('DB_PASS'     , '10271995'),
        os.getenv('DB_HOST'     , 'localhost'),
        os.getenv('DB_PORT'     , 3306),
        os.getenv('DB_NAME'     , 'db')
    ) 
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
#1
    # Assets Management
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')    
    


class ProductionConfig(Config):
  

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
