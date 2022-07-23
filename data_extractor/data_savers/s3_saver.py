import boto3
from datetime import date


class S3Saver:
    file_path = "NewsProject/data_extractor/Output/{}/{}.json"
    bucket_name = "mbucket111111"

    def __init__(self, loader_type):
        self.bucket = boto3.resource('s3').Bucket(self.bucket_name)
        self.file_path = self.file_path.format(str(date.today()), loader_type)

    def save_data(self, data):
        self.bucket.put_object(Key=self.file_path, Body=str(data).encode("utf-8"))
