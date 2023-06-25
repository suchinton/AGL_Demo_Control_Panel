import os

KUKSA_CONFIG = {
    "ip": '10.10.10.203',
    "port": "8090",
    'protocol': 'ws',
    'insecure': True,
}

# fetch token from file from .local/lib/python3.10/site-packages/kuksa_certificates/jwt/super-admin.json.token

TOKEN_PATH = os.path.join(os.path.expanduser("~"), 
                          ".local/lib/python3.10/site-packages/kuksa_certificates/jwt/super-admin.json.token")

print(TOKEN_PATH)
