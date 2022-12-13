from pydantic import BaseSettings, Field


class CustomBaseSettings(BaseSettings):
    """Configure .env settings for all our setting-classes"""

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = True

class Env(CustomBaseSettings):
    SERVICEBUS_CONNECTION_STR: str = Field('', env='sb_connection_string.txt')
    SERVICEBUS_QUEUE_NAME: str = Field('', env='SERVICEBUS_QUEUE_NAME')
    NR_MESSAGES: str = Field('100', env='NR_MESSAGES')
    WAIT_TIME: str = Field('0', env='WAIT_TIME')

env = Env()

class Settings(
    Env
):
    PROJECT_NAME: str = 'autoscale-demo'

settings = Settings()