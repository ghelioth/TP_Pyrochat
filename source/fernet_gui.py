import logging 
import os 
import base64
from basic_gui import BasicGUI, DEFAULT_VALUES
from ciphered_gui import CipheredGUI
import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import hashlib

class FernetGUI (CipheredGUI):
    """
    Classe dérivé de CipheredGUI
    GUI pour un chat client 
    Sécurisé avec l'encryption AES(CTR) et HMAC 
    avec l'utilisation de la bibliothèque Fernet
    """


    def run_chat(self, sender, app_data) -> None:
            # Callback utilisée par la fenêtre de connexion pour démarrer une session de chat
            host = dpg.get_value("connection_host")
            port = int(dpg.get_value("connection_port"))
            name = dpg.get_value("connection_name")
    
            # Récupération du mot de passe
            password = dpg.get_value ("connection_password")

            self._log.info(f"Connecting {name}@{host}:{port}")
    
            # Dérivation de la clef (self.key)
            hash_digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            hash_digest.update(password.encode())
            hash_value = hash_digest.finalize()
            self.key = base64.urlsafe_b64encode(hash_value)

            self._callback = GenericCallback()

            self._client = ChatClient(host, port)
            self._client.start(self._callback)
            self._client.register(name)

            dpg.hide_item("connection_windows")
            dpg.show_item("chat_windows")
            dpg.set_value("screen", "Connecting")

            # sha256().digest()
            self.key = hashlib.sha256(password.encode()).digest()
            self.key = base64.b64decode(self.key)

    
    def encrypt(self, message:str)->bytes:
        # Chiffre le message avec la bibliothèque Fernet

        # Création d'un objet Fernet à partir de la clef dérivée du mot de passe
        f = Fernet(self.key)

        # Chiffrement du message avec Fernet
        encrypted_message = f.encrypt(bytes(message, 'utf-8'))

        return encrypted_message

    def decrypt(self, message:bytes)->str:
        # Déchiffre le message avec la bibliothèque Fernet

        message = base64.b64decode(message['data'])

        # Création d'un objet Fernet à partir de la clef dérivée du mot de passe
        f = Fernet(self.key)

        # Déchiffrement du message avec Fernet
        decrypted_message = f.decrypt(bytes(message, 'utf-8'))

        return decrypted_message.decode()
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = FernetGUI()
    client.create()
    client.loop()
