from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    crm_token: SecretStr
    url: SecretStr

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
