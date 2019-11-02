class BaseConfig:
    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except TypeError:
            raise KeyError(f"config variable '{key}' not found")
