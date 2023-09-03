import os
import platform

python_version = f"python{'.'.join(platform.python_version_tuple()[:2])}"

CA = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/CA.pem"))

KUKSA_CONFIG = {
    "ip": 'localhost',
    "port": "8090",
    'protocol': 'ws',
    'insecure': False,
    'cacertificate': CA,
    'tls_server_name': "Server",
}

TOKEN_PATH = os.path.join(os.path.expanduser("~"), 
                          f".local/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token")