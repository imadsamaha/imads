import logging

import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import BasicGUI, DEFAULT_VALUES
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher,algorithms,modes
import base64
import os 

#iteration
INTERATIONS = 100000
KEY_SIZE = 16
NB_BLOCK = 128
SALT = "data"

class CipheredGUI(BasicGUI):
#Surcharger le constructeur pour y inclure le champ self._key
    def __init__(self) -> None :
        super().__init__()
        self.key = None 

#Surcharger la fonction _create_connection_window()
    def _create_connection_window(self) -> None :
        # windows about connexion
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            for field in ["host", "port", "name"] :
                with dpg.group(horizontal = True) :
                    dpg.add_text(field)
                    dpg.add_input_text(default_value = DEFAULT_VALUES[field], tag = f"connection_{field}")
            
            #add a password 
            dpg.add_text("password")      
            dpg.add_input_text(password = True,tag = f"connection_password")
            dpg.add_button(label = "Connect", callback = self.run_chat)
#Surcharger la fonction run_chat()
    def run_chat(self, sender, app_data) -> None:
         # callback used by the connection windows to start a chat session
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

        #derivation de clef (self._key)
        kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = KEY_SIZE, salt = SALT, iterations = INTERATIONS)
        b_password = bytes(password,"utf8")
        self._key = kdf.derive(b_password)
        self._log.info(f"self.key {self._key}")

#Créer une fonction encrypt()
    def encrypt (self, message):
        iv = os.urandom(KEY_SIZE)
        #algorithme de chiffrement
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv),backend=default_backend()) 
        encryptor = cipher.encryptor()

        #add padding 
        padder = padding.PKCS7(NB_BLOCK).padder()
        padded_message = padder.update(message.encode()) + padder.finalize()
        
 #encrypt the message and return the IV concatenated with the encrypted message
        ciphertext = encryptor.update(padded_message) + encryptor.finalize()
        return (iv,ciphertext)
       
#Créer une fonction decrypt()
    def decrypt(self, message: bytes):
        iv = base64.b64decode(message[0]["data"])
        message = base64.b64decode(message[1]["data"])
        cipher = Cipher( algorithms.AES(self._key), modes.CTR(iv), backend = default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(message) + decryptor.finalize()
        unpadder = padding.PKCS7(NB_BLOCK).unpadder()
        unpadded = unpadder.update(decrypted) + unpadder.finalize()
        return unpadded.decode("utf-8")
    
#Surcharger les fonctions send()/recv()
    def recv(self)->None:
        # function called to get incoming messages and display them
        if self._callback is not None:
            for user, message in self._callback.get():
                user, message = message
                decrypted_message = self.decrypt(message)
                self.update_text_screen(f"{user} : {decrypted_message}")
            self._callback.clear()


    def send(self, text)->None:
        # function called to send a message to all (broadcasting)
        encrypted_message = self.encrypt(text)      
        self._client.send_message(encrypted_message)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()
