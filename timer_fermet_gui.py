import logging
import os
import base64
from basic_gui import BasicGUI, DEFAULT_VALUES
from ciphered_gui import CipheredGUI
from fernet_gui import FernetGUI
import dearpygui.dearpygui as dpg

from chat_client import ChatClient
from generic_callback import GenericCallback
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidToken

import hashlib
import time

class TimeFernetGUI (FernetGUI):
    """
    Classe dérivé de CipheredGUI
    GUI pour un chat client
    Sécurisé avec l'encryption AES(CTR) et HMAC
    avec l'utilisation de la bibliothèque Fernet et gestion du TTL
    """

    def encrypt(self, message:str)->bytes:
    # Chiffre le message avec la bibliothèque Fernet avec gestion du TTL

    # Création d'un objet Fernet à partir de la clef dérivée du mot de passe
    f = Fernet(self.key)

    # Chiffrement du message avec Fernet en ajoutant le temps actuel et le TTL
    encrypted_message = f.encrypt(bytes(message + '-' + str(int(time.time() + self.ttl)), 'utf-8'))

    return encrypted_message

def decrypt(self, message:bytes)->str:
    # Déchiffre le message avec la bibliothèque Fernet avec gestion du TTL et potentiel erreur InvalidToken

    try:
        # Création d'un objet Fernet à partir de la clef dérivée du mot de passe
        f = Fernet(self.key)

        # Déchiffrement du message avec Fernet et extration du temps du message
        decrypted_message = f.decrypt(message)
        decrypted_message, time_str = decrypted_message.decode().split('-')
        time_int = int(time_str)

        # Vérification du TTL
        current_time = int(time.time())
        if current_time > time_int:
            raise InvalidToken

        return decrypted_message
    except InvalidToken:
        self._log.error("Error: invalid token")
        return "Error: invalid token"