
DEFAULT_DBNAME = "market_matcher"
DEFAULT_DRIVER = "sqlite"
DEFAULT_USER = "market_matcher"
DEFAULT_PWD = "market_matcher"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5432


class DBConfig:
    def __init__(self, driver=DEFAULT_DBNAME, dbname=DEFAULT_DBNAME,
                 user=DEFAULT_USER, pwd=DEFAULT_PWD, host=DEFAULT_HOST,
                 port=DEFAULT_PORT) -> None:
        self.driver = driver
        self.dbname = dbname
        self.user = user
        self.pwd = pwd
        self.host = host
        self.port = port
