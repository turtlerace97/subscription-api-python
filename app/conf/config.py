import os
import logging

class Config:
    app_settings = {
        'db_name': os.getenv('DB_NAME'),
        'mongodb_url': os.getenv('MONGO_URL'),
        'db_username': os.getenv('MONGO_USER'),
        'db_password': os.getenv('MONGO_PASSWORD'),
        'jwt_key': os.getenv('JWT_KEY'),
        'jwt_old_key': os.getenv('JWT_OLD_KEY'),
        'jwt_algorithm': os.getenv('JWT_ALGORITHM'),
        'redis_host': os.getenv('REDIS_HOST'),
        'slack_token': os.getenv('SLACK_TOKEN'),
        'aws_region': os.getenv('AWS_REGION'),
        'aws_bucket': os.getenv('AWS_BUCKET'),
        'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
        'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
        'firebase_type': os.getenv('FIREBASE_TYPE'),
        'firebase_project_id': os.getenv('FIREBASE_PROJECT_ID'),
        'firebase_private_key_id': os.getenv('FIREBASE_PRIVATE_KEY_ID'),
        'firebase_private_key': os.getenv('FIREBASE_PRIVATE_KEY'),
        'firebase_client_email': os.getenv('FIREBASE_CLIENT_EMAIL'),
        'firebase_client_id': os.getenv('FIREBASE_CLIENT_ID'),
        'firebase_auth_uri': os.getenv('FIREBASE_AUTH_URI'),
        'firebase_token_uri': os.getenv('FIREBASE_TOKEN_URI'),
        'firebase_auth_provider_cert_url': os.getenv('FIREBASE_AUTH_PROVIDER_CERT_URL'),
        'firebase_client_cert_url': os.getenv('FIREBASE_CLIENT_CERT_URL'),
        'naver_cloud_access_key': os.getenv('NAVER_CLOUD_ACCESS_KEY'),
        'naver_cloud_secret_key': os.getenv('NAVER_CLOUD_SECRET_KEY'),
        'naver_cloud_sms_service_id': os.getenv('NAVER_CLOUD_SMS_SERVICE_ID'),
        's3_file_path': os.getenv('S3_FILE_PATH'),
        's3_update_api': os.getenv('S3_UPDATE_API')
    }

    @classmethod
    def app_setting_validate(cls):
        for k, v in cls.app_settings.items():
            if v is None:
                logging.error(f"Config variable error. {k} cannot be None")
                raise Exception({"msg": "config value not enough"})
            else:
                logging.info(f'Config variable {k} is {v}')

conf = Config()
