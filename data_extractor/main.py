from loader_factory import LoaderFactory
from data_savers.s3_saver import S3Saver


def lambda_handler(event, context):
    loader_type = event["type"]
    loader = LoaderFactory.create_loader(loader_type)
    data = loader.load_data()
    saver = S3Saver(loader_type)
    saver.save_data(data)
    return {"path": saver.file_path}

