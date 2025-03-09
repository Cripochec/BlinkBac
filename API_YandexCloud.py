import logging
import boto3
import hashlib
import base64
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
            config=Config(signature_version='s3v4', s3={'addressing_style': 'virtual'})
        )

        image_stream = BytesIO(photo_data)
        image_stream.seek(0)  # Сбрасываем позицию в начале потока

        # Вычисляем MD5-хеш файла
        md5_hash = hashlib.md5(photo_data).digest()
        md5_base64 = base64.b64encode(md5_hash).decode('utf-8')

        s3_client.upload_fileobj(
            image_stream,
            bucket_name,
            object_name,
            ExtraArgs={'ContentMD5': md5_base64}  # Передаем MD5-хеш
        )

    except Exception as e:
        log_error("upload_photo_to_s3", e)


def get_photo_url(object_name):
    try:
        return f"https://flopy-folder.storage.yandexcloud.net/{object_name}"
    except Exception as e:
        log_error("get_photo_url", e)
