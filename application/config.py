import os


class BaseConfig:
    """ Define base configuration parameters. """

    # Cache blog content, reload this often, in seconds
    BLOG_REFRESH_INTERVAL = 3600 * 12
    BUILD_FRESH_DB = False  # drops all tables and builds them fresh
    DB_SEED_MODULE = None  # path for the seed data to build fresh tables

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except TypeError:
            raise KeyError(f"config variable '{key}' not found")


class BlogDBConfig(BaseConfig):
    """ Defines configuration parameters relevant to the blog database connections. """

    # Sets up the database connection for the blog
    BLOG_DB_PROTOCOL = "mysql://"
    BLOG_DB_HOST = os.environ["MYSQL_LOCAL_HOST"]
    BLOG_DB_USER = os.environ["MYSQL_USER"]
    BLOG_DB_PORT = os.environ["MYSQL_PORT"]
    BLOG_DB_PASSWORD = os.environ["MYSQL_PASSWORD"]
    BLOG_DB_NAME = None

    def get_uri(self) -> str:
        return (
            f"{self.BLOG_DB_PROTOCOL}{self.BLOG_DB_USER}:{self.BLOG_DB_PASSWORD}"
            f"@{self.BLOG_DB_HOST}/{self.BLOG_DB_NAME}"
        )


class DevConfig(BlogDBConfig):
    """ Configuration for development work. """

    BLOG_DB_NAME = os.environ["MYSQL_BLOG_DEV_DB"]
    BUILD_FRESH_DB = True
    DB_SEED_MODULE = "application.testing.seed_db"
    SQLALCHEMY_ECHO = True


class ProdConfig(BlogDBConfig):
    """ Configuration for production """

    BLOG_DB_NAME = os.environ["MYSQL_BLOG_PROD_DB"]
