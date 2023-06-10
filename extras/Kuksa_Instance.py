import kuksa_client as kuksa


class KuksaClientSingleton:
    __instance = None

    @staticmethod
    def get_instance():
        if KuksaClientSingleton.__instance is None:
            KuksaClientSingleton()
        return KuksaClientSingleton.__instance

    def __init__(self):
        if KuksaClientSingleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.default_Config = {
                "ip": '10.10.10.203',
                "port": "8090",
                'protocol': 'ws',
                'insecure': False,
            }

            self.token = "/home/suchinton/.local/lib/python3.10/site-packages/kuksa_certificates/jwt/super-admin.json.token"

            try:
                self.client = kuksa.KuksaClientThread\
                    (self.default_Config)
                self.client.authorize(self.token)
                self.client.start()
            except Exception as e:
                print(e)

            KuksaClientSingleton.__instance = self

    def get_client(self):
        return self.client, self.default_Config, self.token
    
    def get_status(self):
        return self.client.checkConnection()

    def reconnect_client(self, new_Config, new_Token):
        self.client.stop()
        print(self.client.checkConnection())
        self.client = kuksa.KuksaClientThread(new_Config)
        self.client.authorize(new_Token)
        self.client.start()
        return self.client

    def __del__(self):
        self.client.stop()
