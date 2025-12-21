from src.utils.environments import *

API_TITLE = 'Backend'
API_DESCRIPTION = '-'
API_VERSION = 'v1'
API_PREFIX = {
    'static'            : f'/api/{API_VERSION}/static',
    'application'       : f'/api/{API_VERSION}/application',
    'authentication'    : f'/api/{API_VERSION}/authentication',
    'admin'             : f'/api/{API_VERSION}/admin',
    'web_socket'        : f'/api/{API_VERSION}',
}


DATABASE_DRIVERS = {
    'postgresql': 'postgresql+asyncpg',
    'mysql': 'mysql+aiomysql',
    'mariadb': 'mariadb+aiomysql',
    'sqlite': 'sqlite+aiosqlite',
}


