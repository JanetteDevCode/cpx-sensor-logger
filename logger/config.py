import os


config = {
    'dev': {
        'host': os.environ.get('SENSOR_LOG_DEV_SERVER_HOST', '127.0.0.1'),
        'port': os.environ.get('SENSOR_LOG_DEV_SERVER_PORT', '8080'),
        'path': os.environ.get('SENSOR_LOG_DEV_SERVER_PATH', '/api/v1/add'),
        'key': os.environ.get('SENSOR_LOG_DEV_API_POST_KEY', 'apikey')
    },
    'prod': {
        'host': os.environ.get('SENSOR_LOG_PROD_SERVER_HOST', '127.0.0.1'),
        'port': os.environ.get('SENSOR_LOG_PROD_SERVER_PORT', '8080'),
        'path': os.environ.get('SENSOR_LOG_PROD_SERVER_PATH', '/api/v1/add'),
        'key': os.environ.get('SENSOR_LOG_PROD_API_POST_KEY', 'apikey')
    },
}