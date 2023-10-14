"""
   Copyright 2023 Suchinton Chakravarty

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
import platform
from configparser import ConfigParser

python_version = f"python{'.'.join(platform.python_version_tuple()[:2])}"

CA = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/cert/CA.pem"))

KUKSA_CONFIG = {}

WS_TOKEN = os.path.join(os.path.expanduser("~"), f".local/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token")
GRPC_TOKEN = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/token/grpc/actuate-provide-all.token"))

def reload_config():
    KUKSA_CONFIG.clear()
    config = ConfigParser()
    config.read(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini')))
    print(config.sections())

    try:
        preferred_config = config['default']['preferred-config']
    except KeyError:
        preferred_config = None

    if preferred_config:
        try:
            KUKSA_CONFIG['ip'] = config[preferred_config]['ip']
            KUKSA_CONFIG['port'] = config[preferred_config]['port']
            KUKSA_CONFIG['protocol'] = config[preferred_config]['protocol']
            KUKSA_CONFIG['insecure'] = False if config[preferred_config]['insecure'] == 'false' else True
            KUKSA_CONFIG['cacertificate'] = CA if config[preferred_config]['cacert'] == 'true' else None
            KUKSA_CONFIG['tls_server_name'] = config[preferred_config]['tls_server_name'] if config[preferred_config]['tls_server_name'] else None
        except KeyError as e:
            print(f"Error: {e}")
            return None, None

    return KUKSA_CONFIG, GRPC_TOKEN if KUKSA_CONFIG['protocol'] == 'grpc' else WS_TOKEN

print(reload_config())