import logging
from pathlib import Path

from dotenv import load_dotenv


def load_env():
    env_path = Path('..') / '.env'
    load_dotenv(dotenv_path=env_path)


logging.basicConfig(filename='Logs.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
