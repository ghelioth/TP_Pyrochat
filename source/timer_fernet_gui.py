import logging
import base64

from fernet_gui import FernetGUI




from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken

import hashlib
import time

TTL = 30

class TimeFernetGUI (FernetGUI):
    """
    Classe dérivé de CipheredGUI
    GUI pour un chat client
    Sécurisé avec l'encryption AES(CTR) et HMAC
    avec l'utilisation de la bibliothèque Fernet et gestion du TTL
    """
    def __init__(self):
        super().__init__()
        self.ttl = TTL # TTL en secondes

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
            decrypted_message = f.decrypt(bytes(message))
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
        

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = TimeFernetGUI()
    client.create()
    client.loop()