import os
import platform

python_version = "python" + platform.python_version_tuple()[0] + "." + platform.python_version_tuple()[1]

KUKSA_CONFIG = {
    "ip": 'localhost',
    "port": "8090",
    'protocol': 'ws',
    'insecure': False,
}

TOKEN_PATH = os.path.join(os.path.expanduser("~"), 
                          f".local/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token")