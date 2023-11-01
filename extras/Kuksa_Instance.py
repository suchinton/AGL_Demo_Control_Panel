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


class KuksaClientSingleton:
    """
    A singleton class that provides a single instance of KuksaClientThread.

    This class is thread-safe and ensures that only one instance of KuksaClientThread is created.

    Attributes:
        _instance (Optional[KuksaClientSingleton]): The instance of the class.
        _lock (threading.Lock): A lock to ensure thread-safety.
        kuksa_config (dict): The configuration for KuksaClientThread.
        token (str): The path to the token file.
        client (KuksaClientThread): The instance of KuksaClientThread.

    Methods:
        instance() -> KuksaClientSingleton: Returns the instance of the class.
        reconnect(config, token) -> KuksaClientThread: Reconnects the client with the given configuration and token.
        get_client() -> Optional[KuksaClientThread]: Returns the client instance.
        get_config() -> dict: Returns the configuration.
        get_token() -> str: Returns the path to the token file.
        status() -> bool: Returns the status of the client connection.
    """

    _instance: Optional["KuksaClientSingleton"] = None
    _lock = threading.Lock()

    @staticmethod
    def instance() -> "KuksaClientSingleton":
        """
        Returns the instance of the class.

        If the instance does not exist, it creates a new instance.

        Returns:
            KuksaClientSingleton: The instance of the class.
        """
        if KuksaClientSingleton._instance is None:
            with KuksaClientSingleton._lock:
                if KuksaClientSingleton._instance is None:
                    KuksaClientSingleton._instance = KuksaClientSingleton()
        return KuksaClientSingleton._instance

    def __init__(self):
        """
        Initializes the class.

        If the instance already exists, it raises an exception.

        It initializes the configuration, token and client instance.
        """
        if KuksaClientSingleton._instance is not None:
            raise Exception("This class is a singleton!")

        self.client = None
        self.kuksa_config = None

        KuksaClientSingleton._instance = self

    def reconnect(self, config, token):
        """
        Reconnects the client with the given configuration and token.

        Args:
            config (dict): The configuration for KuksaClientThread.
            token (str): The path to the token file.

        Returns:
            KuksaClientThread: The instance of KuksaClientThread.
        """
        if self.client:
            self.client.stop()
        self.kuksa_config = config
        self.token = token
        self.client = kuksa.KuksaClientThread(self.kuksa_config)
        self.client.authorize(self.token)
        self.client.start()

    def get_client(self):
        """
        Returns the client instance.

        Returns:
            Optional[KuksaClientThread]: The instance of KuksaClientThread.
        """
        if self.client:
            return self.client
        else:
            return None

    def get_config(self):
        """
        Returns the configuration.

        Returns:
            dict: The configuration for KuksaClientThread.
        """
        return self.kuksa_config
    
    def get_token(self):
        """
        Returns the path to the token file.

        Returns:
            str: The path to the token file.
        """
        return self.token

    def status(self):
        """
        Returns the status of the client connection.

        Returns:
            bool: The status of the client connection.
        """
        return self.client.checkConnection() if self.client else False

    def __del__(self):
        """
        Stops the client instance.
        """
        if self.client:
            self.client.stop()
