from LoaderFactory import LoaderFactory
from DataSavers.S3Saver import S3Saver
from datetime import date


def lambda_handler(event, context):
    type = event["type"]
    loader = LoaderFactory.create_loader(type)
    data = loader.load_data()
    file_path = "NewsProject/Data Extractor/Output/" + str(date.today()) + "/" + type + ".json"
    bucket = "mbucket111111"
    saver = S3Saver(bucket)
    saver.save_data(data, file_path)
    return {"path": file_path}
