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
import threading

class FeedKuksa(QThread):
    """
    A class to handle sending values to Kuksa.

    Attributes:
    -----------
    stop_flag : bool
        A flag to stop the thread.
    kuksa : kuksa_instance.KuksaClientSingleton.instance()
        An instance of the Kuksa client.
    client : kuksa_instance.KuksaClientSingleton.instance().client
        A client object to interact with the Kuksa server.
    """

    def __init__(self, parent=None):
        """
        Constructs all the necessary attributes for the FeedKuksa object.

        Parameters:
        -----------
        parent : QObject
            The parent object of the FeedKuksa object.
        """
        QThread.__init__(self,parent)
        self.stop_flag = False

    def run(self):
        """
        Starts the thread and sets the instance of the Kuksa client.
        """
        logging.info("Starting thread")
        self.set_instance()

    def stop(self):
        """
        Stops the thread.
        """
        self.stop_flag = True
        
        logging.info("Stopping thread")

    def set_instance(self):
        """
        Sets the instance of the Kuksa client.
        """
        self.kuksa = kuksa_instance.KuksaClientSingleton.instance()
        self.client = self.kuksa.get_client()

    def send_values(self, path=None, value=None, attribute=None):
        """
        Sends values to Kuksa.

        Parameters:
        -----------
        path : str
            The path to the value in Kuksa.
        value : str
            The value to be sent to Kuksa.
        attribute : str
            The attribute of the value in Kuksa.

        Raises:
        -------
        Exception
            If there is an error sending values to Kuksa.
        """
        if self.client is None:
            logging.error("Kuksa client is None, try reconnecting")
            return

        if not self.client.checkConnection():
            logging.error("Kuksa client is not connected, try reconnecting")
            threading.Thread(target=self.set_instance).start()
            return

        try:
            if attribute is not None:
                self.client.setValue(path, value, attribute)
            else:
                self.client.setValue(path, value)
        except Exception as e:
            logging.error(f"Error sending values to kuksa {e}")
            threading.Thread(target=self.set_instance).start()