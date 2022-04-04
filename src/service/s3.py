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
    S3.upload_fileobj(file, configs.BUCKET_NAME, path)
    url = S3.generate_presigned_url('get_object', Params={'Bucket': configs.BUCKET_NAME, 'Key': path}, ExpiresIn=604799)
    return url
