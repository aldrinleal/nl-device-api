from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "nl-da"
    DEBUG: bool = False
    #ROOT_PATH: str


settings = Settings()
