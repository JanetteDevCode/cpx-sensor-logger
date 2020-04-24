import os


config = {
    'dev': {
        'host': os.environ.get('SENSOR_LOG_DEV_SERVER_HOST', '127.0.0.1'),
        'port': os.environ.get('SENSOR_LOG_DEV_SERVER_PORT', '8080'),
        'key': os.environ.get('SENSOR_LOG_DEV_API_POST_KEY', 'apikey')
    },
    'prod': {
        'host': os.environ.get('SENSOR_LOG_PROD_SERVER_HOST', '127.0.0.1'),
        'port': os.environ.get('SENSOR_LOG_PROD_SERVER_PORT', '8080'),
        'key': os.environ.get('SENSOR_LOG_PROD_API_POST_KEY', 'apikey')
    },
}