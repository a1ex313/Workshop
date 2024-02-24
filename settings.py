from pydantic_settings import BaseSettings
#from workshop.Create_tables import pp


#pp()
print("settings")

class Settings(BaseSettings):
    server_host: str = '127.0.0.1'
    server_port: int = 3306
    database_url: str


    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600



settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
