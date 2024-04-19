from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Classe das variaveis de ambiente do projeto
    """

    ENVIROMENT: str = "local"
    LOG_ENVIROMENT: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache
def return_default_settings() -> Settings:
    """
    Chamamos sempre essa função com os valores em cache
    para evitar aumento de memoria desnecessário.
    """
    return Settings()
