from ciphered_gui import CipheredGUI
import logging
import dearpygui.dearpygui as dpg
from chat_client import ChatClient
from cryptography.fernet import Fernet
from generic_callback import GenericCallback
import base64
import hashlib

class FernetGUI(CipheredGUI) :
    def run_chat(self, sender, app_data)-> None:
    
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

      
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")
         # generating password
        self.key = hashlib.sha256(password.encode()).digest()
        self.key = base64.b64encode(self.key)

    def encrypt(self, message):
        '''
        chiffre le message avec Fernet
        '''
    
        cipher = Fernet(self.key)
        message = bytes(message,"utf-8")
        return cipher.encrypt(message)
    
    def decrypt(self, message: bytes):
        message = base64.b64decode(message["data"])
        cipher= Fernet(self.key)
        return cipher.decrypt(message).decode("utf-8")
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()