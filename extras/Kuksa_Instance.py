import kuksa_client as kuksa
import threading
import time

class KuksaClientSingleton:
    __instance = None
    __lock = threading.Lock()

    @staticmethod
    def get_instance():
        if KuksaClientSingleton.__instance is None:
            with KuksaClientSingleton.__lock:
                if KuksaClientSingleton.__instance is None:
                    KuksaClientSingleton.__instance = KuksaClientSingleton()
        return KuksaClientSingleton.__instance

    def __init__(self):
        if KuksaClientSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.default_Config = {
                "ip": '10.10.10.203',
                "port": "8090",
                'protocol': 'ws',
                'insecure': True,
            }

            self.token = "/home/suchinton/.local/lib/python3.10/site-packages/kuksa_certificates/jwt/super-admin.json.token"

            try:
                self.client = kuksa.KuksaClientThread(self.default_Config)
                self.client.authorize(self.token)
                time.sleep(2)
                if self.client.checkConnection() == False:
                    self.client = None
            except Exception as e:
                print(e)
                

            KuksaClientSingleton.__instance = self

    def reconnect_client(self, new_Config, new_Token):
        if self.client is not None:
            self.client.stop()
        self.client = kuksa.KuksaClientThread(new_Config)
        self.client.authorize(new_Token)
        return self.client

    def get_client(self):
        return self.client        
    
    def get_config(self):
        return self.default_Config
    
    def get_token(self):
        return self.token

    def get_status(self):
        return self.client.checkConnection()

    def __del__(self):
        self.client.stop()
