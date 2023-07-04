import os
import platform

python_version = "python" + platform.python_version_tuple()[0] + "." + platform.python_version_tuple()[1]

KUKSA_CONFIG = {
    "ip": '10.10.10.203',
    "port": "8090",
    'protocol': 'ws',
    'insecure': True,
}

TOKEN_PATH = os.path.join(os.path.expanduser("~"), 
                          f".local/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token")