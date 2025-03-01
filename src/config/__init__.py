from .settings import Settings

# Instantiate the settings object
settings = Settings()

# Optionally, control what’s exposed when importing from the package
__all__ = ['settings']