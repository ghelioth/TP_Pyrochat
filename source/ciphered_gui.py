import logging 
import os
import base64

from basic_gui import BasicGUI, DEFAULT_VALUES

import dearpygui.dearpygui as dpg

from chat_client import ChatClient 
from generic_callback import GenericCallback
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Variables
taille_bloc = 128
nb_itteration = 10000
octets = 16

    
class CipheredGUI (BasicGUI):
    """
    Classe derivé de la classe BasicGUI
    GUI pour un chat client.
    Sécurisé avec l'encrytion AES(CTR) 
    """
    def __init__(self)->None:
            #Surcharge du constructeur 
            super().__init__()
            self.key = None





    def _create_connection_window(self)->None:
        # windows about connexion
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
            
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            
            # Ajout d'un champ pour la saisie du mot de passe 
            with dpg.group(horizontal = True) :
                dpg.add_text(" pwd")
                dpg.add_input_text(password = True, tag = "connection_password")

            dpg.add_button(label="Connect", callback=self.run_chat)



    def run_chat(self, sender, app_data)->None:
        # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        
        # Récupération du mot de passe
        password = dpg.get_value ("connection_password")

        self._log.info(f"Connecting {name}@{host}:{port}")
        
        # Dérivation de la clef (self.key)
        salt = b'Helioth' # utilisation de Helioth comme salt constant hihi

        kdf = PBKDF2HMAC(algorithm = hashes.SHA256(), length = 32, salt = salt, iterations = nb_itteration, backend = default_backend())
        self.key = kdf.derive(password.encode())

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")
    
    def encrypt (self, message : str) -> tuple :
        # chiffre le message avec l'encryption AES(CTR)

        gh = os.urandom(octets)
        gh_bytes = bytes(gh)
        hw = Cipher(algorithms.AES(self.key), modes.CTR(gh_bytes), backend = default_backend())
        encrytion = hw.encryptor()
        
        pad = padding.PKCS7(taille_bloc).padder()

        pad_d = pad.update(message.encode()) + pad.finalize()
        hw_txt = encrytion.update(pad_d) + encrytion.finalize()

        return gh, hw_txt
    
    def decrypt (self, message : tuple) -> str :
        # Déchiffrage du message avec l'encryption AES(CTR)
        # Recuperation de gh et du message en base64
        gh = base64.b64decode(message[0]['data'])
        hw_txt = base64.b64decode(message[1]['data'])

        gw = Cipher(algorithms.AES(self.key), modes.CTR(gh), backend = default_backend())
        decryptage = gw.decryptor()
        u_pad = padding.PKCS7(algorithms.AES.block_size).unpadder()

        pad_d = decryptage.update(hw_txt) + decryptage.finalize()
        donnee = u_pad.update(pad_d) + u_pad.finalize()

        return donnee.decode()


    def recv(self)->None:
        # Surcharge de la fonction recv () pour faire intervenir decrypt()
        # dechiffre le message reçu du serveur 
        if self._callback is not None :
            for user, message in self._callback.get() :
                message_decrypte = self.decrypt(message)
                self.update_text_screen(f"{user} : {message_decrypte}")
            
            self._callback.clear()

    def send(self, text)->None:
        # Surcharge de la fonction send()
        # Chiffrement du message avant de l'envoyer au serveur 
        message_chiffre = self.encrypt(text)
        super().send(message_chiffre)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()