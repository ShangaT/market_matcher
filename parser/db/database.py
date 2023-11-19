import os
from dotenv import load_dotenv
from peewee import *

if not os.environ.get('DOCKER', 0):
    load_dotenv('./.env.local')

if os.environ.get('DATABASE', 'sqlite') == 'postgres':
    db = PostgresqlDatabase(os.environ.get('SQL_DATABASE', 'market_matcher_dev'),
                            user=os.environ.get('SQL_USER', 'postgres'),
                            password=os.environ.get(
                                'SQL_PASSWORD', 'postgres'),
                            host=os.environ.get('SQL_HOST', 'postgres'),
                            port=os.environ.get('SQL_PORT', 'postgres'),
                            )
else:
    db = SqliteDatabase(os.environ.get('SQL_DATABASE')+'.db')
