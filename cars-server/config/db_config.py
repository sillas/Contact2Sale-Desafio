import pymongo
from pymongo.errors import ServerSelectionTimeoutError
from bson.codec_options import CodecOptions

from config.logger import logger


class ConfigDB:

    db = None
    collection = None
    socketTimeoutMS = None
    serverSelectionTimeoutMS = None

    def __init__(self, socketTimeoutMS=3000, serverSelectionTimeoutMS=3000):
        self.socketTimeoutMS = socketTimeoutMS
        self.serverSelectionTimeoutMS = serverSelectionTimeoutMS
        self.db = None
        self.collection = None

        self.config()

    def config(self):
        try:
            client = pymongo.MongoClient(
                "mongodb://localhost:27017/",
                serverSelectionTimeoutMS=self.serverSelectionTimeoutMS,
                socketTimeoutMS=self.socketTimeoutMS
            )

            client.server_info()

            # Configure database with codec options
            codec_options = CodecOptions(
                unicode_decode_error_handler='replace')

            self.db = client.get_database(
                "mcp_server", codec_options=codec_options)
            self.collection = self.db.get_collection(
                "cars_catalog", codec_options=codec_options)
            logger.info("Database Started")

        except ServerSelectionTimeoutError:
            error_message = "Não foi possível conectar ao servidor MongoDB. Verifique se o serviço está em execução."
            logger.exception(error_message)
            raise


db = ConfigDB()
