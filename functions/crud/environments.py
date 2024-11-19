from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent

class Environments(BaseSettings):
    TABLE_NAME: str
    REGION: str
    model_config = SettingsConfigDict(env_file=f'{ROOT_DIR}/.env', env_file_encoding='utf-8')

env = Environments()