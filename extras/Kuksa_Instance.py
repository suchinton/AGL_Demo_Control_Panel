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

from typing import Optional
import kuksa_client as kuksa
import threading
import time

from extras import config

class KuksaClientSingleton:
    _instance: Optional["KuksaClientSingleton"] = None
    _lock = threading.Lock()

    @staticmethod
    def instance() -> "KuksaClientSingleton":
        if KuksaClientSingleton._instance is None:
            with KuksaClientSingleton._lock:
                if KuksaClientSingleton._instance is None:
                    KuksaClientSingleton._instance = KuksaClientSingleton()
        return KuksaClientSingleton._instance

    def __init__(self):
        if KuksaClientSingleton._instance is not None:
            raise Exception("This class is a singleton!")

        self.config = config.KUKSA_CONFIG
        self.token = config.TOKEN_PATH

        try:
            self.client = kuksa.KuksaClientThread(self.config)
            self.client.authorize(self.token)
            time.sleep(2)
            if not self.client.checkConnection():
                self.client = None
        except Exception as e:
            print(e)

        KuksaClientSingleton._instance = self

    def reconnect(self, config, token):
        if self.client:
            self.client.stop()
        self.client = kuksa.KuksaClientThread(config)
        self.client.authorize(token)
        return self.client

    def get_client(self):
        if self.client:
            return self.client
        else:
            return None
        
    def get_config(self):
        return self.config
    
    def get_token(self):
        return self.token

    def status(self):
        return self.client.checkConnection() if self.client else False

    def __del__(self):
        if self.client:
            self.client.stop()