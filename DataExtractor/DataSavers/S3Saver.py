import boto3


class S3Saver:
    def __init__(self, bucket_name):
        self.bucket = boto3.resource('s3').Bucket(bucket_name)

    def save_data(self, data, file_path):
        self.bucket.put_object(Key=file_path, Body=str(data).encode("utf-8"))
