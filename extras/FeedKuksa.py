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
from PyQt5.QtCore import QThread
from . import Kuksa_Instance as kuksa_instance

class FeedKuksa(QThread):
    def __init__(self, parent=None):
        QThread.__init__(self,parent)
        self.stop_flag = False
        self.set_instance()

    def run(self):
        print("Starting thread")
        self.set_instance()
        while not self.stop_flag:
            self.send_values()

    def stop(self):
        self.stop_flag = True
        print("Stopping thread")

    def set_instance(self):
        self.kuksa = kuksa_instance.KuksaClientSingleton.get_instance()
        self.client = self.kuksa.get_client()

    def send_values(self, Path=None, Value=None, Attribute=None):
        if self.client is not None:
            if self.client.checkConnection() is True:

                if Attribute is not None:
                    self.client.setValue(Path, Value, Attribute)
                else:
                    self.client.setValue(Path, Value)
            else:
                print("Could not connect to Kuksa")
                self.set_instance()
        else:
            print("Kuksa client is None, try reconnecting")
            time.sleep(2)
            self.set_instance()