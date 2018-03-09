import logging
import sys

storage_host = '0.0.0.0'
storage_user = 'xqa'
storage_password = 'xqa'
storage_database_name = 'xqa'

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format="%(asctime)s  %(levelname)8s --- [%(threadName)20s]: %(funcName)25s, %(lineno)3s: %(message)s")
