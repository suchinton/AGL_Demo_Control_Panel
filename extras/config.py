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

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))

config = ConfigParser()
config.read(CONFIG_PATH)

KUKSA_CONFIG = {}
KUKSA_TOKEN = None

def select_config(preferred_config):
    KUKSA_CONFIG.clear()

    if config.has_section(preferred_config):
        KUKSA_CONFIG['ip'] = config[preferred_config]['ip']
        KUKSA_CONFIG['port'] = config[preferred_config]['port']
        KUKSA_CONFIG['protocol'] = config[preferred_config]['protocol']
        KUKSA_CONFIG['insecure'] = False if config[preferred_config]['insecure'] == 'false' else True
        KUKSA_CONFIG['cacertificate'] = (config.has_option(preferred_config, 'cacert') and config[preferred_config]['cacert'] == 'true')
        KUKSA_TOKEN = GRPC_TOKEN if KUKSA_CONFIG['protocol'] == 'grpc' else WS_TOKEN
    else:
        raise ValueError(f"Config section {preferred_config} not found in config.ini")

    return preferred_config, KUKSA_CONFIG , KUKSA_TOKEN

def get_list_configs():
    return config.sections()[1:]

def get_default_config():
    defaultConfigName = config.get('default', 'preferred-config')
    return defaultConfigName