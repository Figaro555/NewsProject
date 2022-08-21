from pyspark.sql import SparkSession

from loaders.s3_bucket import S3Bucket


def main():
    ss = SparkSession \
        .builder \
        .master("local[*]") \
        .getOrCreate()

    ss.sparkContext.setLogLevel("ERROR")

    bucket = S3Bucket()

    files = ss.sparkContext.parallelize(bucket.get_files_in_folder())
    raw_data = files.flatMap(lambda file: bucket.load_data(file))

    if raw_data.count() == 0:
        return


if __name__ == '__main__':
    main()
