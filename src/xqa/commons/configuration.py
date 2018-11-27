import logging
import sys

sqlite_host = '0.0.0.0'
sqlite_user = 'xqa'
sqlite_password = 'xqa'
sqlite_name = 'xqa'

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="%(asctime)s.%(msecs)03d  %(levelname)8s --- [%(process)5d] %(filename)25s:%(funcName)30s, %(lineno)3s: %(message)s")

logging.getLogger('docker').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logging.getLogger('matplotlib').setLevel(logging.WARNING)
