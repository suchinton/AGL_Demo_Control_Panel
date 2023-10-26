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


def check_paths(*paths):
    return {path: os.path.exists(path) for path in paths}


CONFIG_PATHS = check_paths(
    "/etc/agl-demo-control-panel.ini",
    os.path.join(os.path.expanduser("~"),
                 ".local/share/agl-demo-control-panel/config.ini"),
    os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
)

CA_PATHS = check_paths(
    "/etc/kuksa-val/CA.pem",
    f"/usr/lib/{python_version}/site-packages/kuksa_certificates/CA.pem",
    os.path.abspath(os.path.join(os.path.dirname(
        __file__), "../assets/cert/CA.pem"))
)

WS_TOKEN_PATHS = check_paths(
    f"/usr/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token",
    os.path.join(os.path.expanduser(
        "~"), f".local/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token")
)

GRPC_TOKEN_PATHS = check_paths(
    f"/usr/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token",
    os.path.abspath(os.path.join(os.path.dirname(__file__),
                    "../assets/token/grpc/actuate-provide-all.token"))
)

config = ConfigParser()
config_path = next((path for path, exists in CONFIG_PATHS.items() if exists), None)
if config_path:
    config.read(config_path)

CA_PATH = next((path for path, exists in CA_PATHS.items() if exists), None)
WS_TOKEN = next((path for path, exists in WS_TOKEN_PATHS.items() if exists), None)
GRPC_TOKEN = next((path for path, exists in GRPC_TOKEN_PATHS.items() if exists), None)

KUKSA_CONFIG = {}
KUKSA_TOKEN = None

def select_config(preferred_config):
    """
    Selects a configuration from the config.ini file based on the preferred_config parameter.

    Args:
        preferred_config (str): The name of the configuration section to select.

    Returns:
        Tuple[str, Dict[str, Union[str, bool]], str]: A tuple containing the name of the selected configuration section,
        a dictionary containing the configuration options for the selected section, and the token to use for the selected
        protocol.
    """
    global KUKSA_CONFIG, KUKSA_TOKEN
    KUKSA_CONFIG.clear()

    if config.has_section(preferred_config):
        KUKSA_CONFIG['ip'] = config[preferred_config]['ip']
        KUKSA_CONFIG['port'] = config[preferred_config]['port']
        KUKSA_CONFIG['protocol'] = config[preferred_config]['protocol']
        KUKSA_CONFIG['insecure'] = False if config[preferred_config]['insecure'] == 'false' else True

        if config.has_option(preferred_config, 'cacert'):
            KUKSA_CONFIG['cacertificate'] = config[preferred_config]['cacert'] if os.path.exists(
                config[preferred_config]['cacert']) else CA_PATH
        else:
            KUKSA_CONFIG['cacertificate'] = None

        KUKSA_CONFIG['tls_server_name'] = config[preferred_config]['tls_server_name']

        if config.has_option(preferred_config, 'token'):
            if config[preferred_config]['token'] == 'default':
                KUKSA_TOKEN = get_default_token(KUKSA_CONFIG['protocol'])
            elif os.path.exists(config[preferred_config]['token']):
                KUKSA_TOKEN = config[preferred_config]['token']
        else:
            ValueError(
                f"Token file {config[preferred_config]['token']} not found")
    else:
        raise ValueError(
            f"Config section {preferred_config} not found in config.ini")

    return preferred_config, KUKSA_CONFIG, KUKSA_TOKEN


def get_list_configs():
    return config.sections()[1:]


def get_default_config():
    defaultConfigName = config.get('default', 'preferred-config')
    return defaultConfigName


def get_default_token(protocol):
    if protocol == 'grpc':
        return GRPC_TOKEN
    else:
        return WS_TOKEN


def save_session_config(session_config, auth_token, CA_File=None):
    """
    save values to config.ini under [user-session]
    """

    config.set('user-session', 'ip', str(session_config['ip']))
    config.set('user-session', 'port', str(session_config['port']))
    config.set('user-session', 'protocol', str(session_config['protocol']))
    config.set('user-session', 'insecure', str(session_config['insecure']))
    config.set('user-session', 'tls_server_name',
               str(session_config['tls_server_name']))
    if auth_token in WS_TOKEN_PATHS or auth_token in GRPC_TOKEN_PATHS or auth_token == 'default':
        config.set('user-session', 'token', 'default')
    else:
        config.set('user-session', 'token', str(auth_token))

    if CA_File in CA_PATHS or CA_File == 'default':
        config.set('user-session', 'cacert', 'default')
    else:
        config.set('user-session', 'cacert', str(CA_File))

    with open(config_path, 'w') as configfile:
        config.write(configfile)


def fullscreen_mode():
    return config.getboolean('default', 'fullscreen-mode')


if not config.has_section('user-session'):
    config.add_section('user-session')
    temp = {
        'ip': "",
        'port': "",
        'protocol': "",
        'insecure': "",
        'cacert': "",
        'token': "",
        'tls_server_name': "",
    }
    save_session_config(temp, 'default', 'default')