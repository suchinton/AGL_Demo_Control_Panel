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

import time
import logging
from PyQt5.QtCore import QThread
from . import Kuksa_Instance as kuksa_instance

class FeedKuksa(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        self.stop_flag = False

    def run(self):
        logging.info("Starting thread")
        self.set_instance()

    def stop(self):
        self.stop_flag = True
        logging.info("Stopping thread")

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
        self.client = self.kuksa.client

    def send_values(self, path=None, value=None, attribute=None):
        if self.client is not None:
            if self.client.checkConnection():
                try:
                    if attribute is not None:
                        self.client.setValue(path, str(value), attribute)
                    else:
                        self.client.setValue(path, str(value))
                except Exception as e:
                    logging.error(f"Error sending values to kuksa {e}")
                    self.set_instance()
        else:
            logging.error("Kuksa client is None, try reconnecting")
            time.sleep(2)
            self.set_instance()