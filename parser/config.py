import os

from dotenv import load_dotenv
from db.config import *


class Config:
    def __init__(self, docker=False, dbconfig: DBConfig = DBConfig()) -> None:
        self.docker = docker
        self.dbconfig = dbconfig

    def read_from_env(self):
        self.docker = os.environ.get("DOCKER", 0)

        if self.docker == 1:
            load_dotenv('.env.dev')
        else:
            load_dotenv('.env.local')

        self.dbconfig = DBConfig(
            driver=os.environ.get("DRIVER", DEFAULT_DRIVER),
            dbname=os.environ.get("SQL_DB", DEFAULT_DBNAME),
            user=os.environ.get("SQL_USER", DEFAULT_USER),
            pwd=os.environ.get("SQL_PWD", DEFAULT_PWD),
            host=os.environ.get("SQL_HOST", DEFAULT_HOST),
            port=os.environ.get("SQL_PORT", DEFAULT_PORT),
        )
