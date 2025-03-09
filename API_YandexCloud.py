import logging
import boto3
from botocore.exceptions import NoCredentialsError
from botocore.config import Config
from io import BytesIO

# Настройка логирования
logging.basicConfig(
    filename='LOGGING.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(message)s'
)


def log_error(route_name, error):
    logging.error(f'S3, API.py ({route_name}): {error}')


def delete_photo_from_s3(object_name):
    try:
        bucket_name = 'flopy-folder'
        s3_client = boto3.client(
            's3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id='YCAJESYKeslrDhzmpCLJMfShP',
            aws_secret_access_key='YCMQ8fFvl0Zu1sosm15WzsAUgRvSLZIU_lAU8een',
            region_name='ru-central1',
            config=Config(signature_version='s3v4')
        )
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)
    except Exception as e:
        log_error("delete_photo_from_s3", e)


def upload_photo_to_s3(photo_data, object_name):
    try:
        if not photo_data:
            raise ValueError("photo_data is empty or None")

        bucket_name = 'flopy-folder'
        s3_client = boto3.client(
            's3',
            endpoint_url='https://storage.yandexcloud.net',
            aws_access_key_id='YCAJESYKeslrDhzmpCLJMfShP',
            aws_secret_access_key='YCMQ8fFvl0Zu1sosm15WzsAUgRvSLZIU_lAU8een',
            region_name='ru-central1',
            config=Config(signature_version='s3v4')
        )

        image_stream = BytesIO(photo_data)
        image_stream.seek(0)  # ВАЖНО!

        s3_client.upload_fileobj(image_stream, bucket_name, object_name)

    except Exception as e:
        log_error("upload_photo_to_s3", e)

def get_photo_url(object_name):
    try:
        return f"https://flopy-folder.storage.yandexcloud.net/{object_name}"
    except Exception as e:
        log_error("get_photo_url", e)
