import os
from pydantic_settings import BaseSettings

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

class Config(BaseSettings):
    PROXY_USER: str
    PROXY_PASS: str
    PROXY_IP: str
    PROXY_PORT: str

    class Config:
        env_file = os.path.join(ROOT_DIR, '.env')
        env_file_encoding = 'utf-8'


env = Config()

