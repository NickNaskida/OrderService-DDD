from src.core.settings import settings


def get_postgres_uri():
    """Returns the URI for the Postgres database."""
    host, port = settings.POSTGRES_HOST, settings.POSTGRES_PORT
    user, password, db_name = settings.POSTGRES_USER, settings.POSTGRES_PASSWORD, settings.POSTGRES_DB
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_redis_uri():
    """Returns the URI for the Redis database."""
    host, port = settings.REDIS_HOST, settings.REDIS_PORT
    db = settings.REDIS_DB
    return f"redis://{host}:{port}/{db}"


def get_api_url():
    """Returns the URL for the API."""
    host, port = settings.API_HOST, settings.API_PORT
    api_url = settings.API_V1_STR
    return f"http://{host}:{port}" + api_url
