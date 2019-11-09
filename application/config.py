import os


class BaseConfig:
    # Cache blog content, reload this often
    BLOG_REFRESH_INTERVAL = 3600 * 12

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except TypeError:
            raise KeyError(f"config variable '{key}' not found")


class BlogDBConfig(BaseConfig):
    # Sets up the database connection for the blog
    BLOG_DB_PROTOCOL = "mysql"
    BLOG_DB_HOST = os.environ["MYSQL_LOCAL_HOST"]
    BLOG_DB_USER = os.environ["MYSQL_USER"]
    BLOG_DB_PORT = os.environ["MYSQL_PORT"]
    BLOG_DB_PASSWORD = os.environ["MYSQL_PASSWORD"]
    BLOG_DB_NAME = None

    def get_uri(self) -> str:
        return (
            f"{self.BLOG_DB_PROTOCOL}://{self.BLOG_DB_USER}"
            f":{self.BLOG_DB_PASSWORD}@{self.BLOG_DB_HOST}"
            f"/{self.BLOG_DB_NAME}"
        )


class DevConfig(BlogDBConfig):
    BLOG_DB_NAME = os.environ["MYSQL_BLOG_DEV_DB"]


class ProdConfig(BlogDBConfig):
    BLOG_DB_NAME = os.environ["MYSQL_BLOG_PROD_DB"]

