import logging
from pathlib import Path

from dotenv import load_dotenv


def load_env():
    dir_of_script = Path(__file__).parent
    env_path = dir_of_script.parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)


logging.basicConfig(filename='Logs.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
