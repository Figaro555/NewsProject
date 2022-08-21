from pyspark.sql import SparkSession

from config.words_to_find import words
from loaders.s3_bucket import S3Bucket
from transformers.rdd_transformer import RDDTransformer


def main():
    ss = SparkSession \
        .builder \
        .master("local[*]") \
        .getOrCreate()

    ss.sparkContext.setLogLevel("ERROR")

    bucket = S3Bucket()
    rdd_trans = RDDTransformer()

    files = ss.sparkContext.parallelize(bucket.get_files_in_folder())
    raw_data = files.flatMap(lambda file: bucket.load_data(file))

    if raw_data.count() == 0:
        return

    data_with_finding = raw_data.map(lambda row: rdd_trans.find_words(row, words))


if __name__ == '__main__':
    main()
