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

python_version = f"python{'.'.join(platform.python_version_tuple()[:2])}"

CA = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/cert/CA.pem"))

KUKSA_CONFIG = {
    "ip": '10.42.0.95',
    "port": "8090",
    'protocol': 'ws',
    'insecure': False,
    'cacertificate': CA,
    'tls_server_name': "Server",
}

WS_TOKEN = os.path.join(os.path.expanduser("~"), f".local/lib/{python_version}/site-packages/kuksa_certificates/jwt/super-admin.json.token")
GRPC_TOKEN = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/token/grpc/actuate-provide-all.token"))