import logging
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    app_settings = {
        'db_name': os.getenv('DB_NAME'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'db_username': os.getenv('MONGO_USER'),
        'db_password': os.getenv('MONGO_PASSWORD'),
    }

    @classmethod
    def app_setting_validate(cls):
        for k, v in cls.app_settings.items():
            if v is None:
                logging.error(f"Config variable error. {k} cannot be None")
                raise Exception({"msg":"config value not enough"})
            else:
                logging.info(f'Config variable {k} is {v}')

    
