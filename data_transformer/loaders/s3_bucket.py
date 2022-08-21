import json
from datetime import date

import boto3
from pyspark.sql import DataFrame


class S3Bucket:
    bucket = boto3.client("s3")
    current_date = str(date.today())
    bucket_name = "mbucket111111"

    def get_files_in_folder(self):
        response = self.bucket.list_objects_v2(
            Bucket=self.bucket_name,
            Prefix='NewsProject/Data Extractor/Output/' + self.current_date
        )
        return [i["Key"] for i in response["Contents"]]

    def load_data(self, file):
        response = self.bucket.get_object(Bucket=self.bucket_name, Key=file)
        data = response['Body'].read().decode('UTF-8')
        return json.loads(data)

