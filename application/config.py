class BaseConfig:
    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except TypeError:
            raise KeyError(f"config variable '{key}' not found")


class Config(BaseConfig):
    BLOG_REFRESH_INTERVAL = 3600 * 12  # Cache blog content, for reload this often

