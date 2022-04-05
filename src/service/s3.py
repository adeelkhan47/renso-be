from time import time

import boto3 as boto3

from configuration import configs

S3 = boto3.client(service_name='s3',
                  region_name='us-east-2',
                  aws_access_key_id=configs.S3_ACCESS_KEY_ID,
                  aws_secret_access_key=configs.S3_ACCESS_KEY
                  )


def upload_image(file):
    file_type = file.content_type.split("/")[1]
    path = f"images/{str(float(time())).replace('.', '')}.{file_type}"
    S3.upload_fileobj(Fileobj=file, Bucket=configs.BUCKET_NAME, Key=path,
                      ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/jpeg'})
    url = f"https://rensoimages.s3.amazonaws.com/{path}"
    return url
