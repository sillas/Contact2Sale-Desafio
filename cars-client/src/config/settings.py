import sys
import logging
from dotenv import load_dotenv

load_dotenv()

class InfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

class NonInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno != logging.INFO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Handler para o console (apenas INFO)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.addFilter(InfoFilter())
console_handler.setFormatter(logging.Formatter('%(message)s'))

# Handler para arquivo (tudo exceto INFO)
file_handler = logging.FileHandler('client_app.log')
file_handler.setLevel(logging.DEBUG)
file_handler.addFilter(NonInfoFilter())
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Adicionar handlers ao logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)