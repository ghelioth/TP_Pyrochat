import logging, os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding, hashes, kdf
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import dearpygui.dearpygui as dpg
import serpent

from basic_gui import BasicGUI, DEFAULT_VALUES
from chat_client import ChatClient
from generic_callback import GenericCallback


class CipheredGUI(BasicGUI):
    def init(self)->None:
        super().__init__()
        self._key = None

    def _create_connection_window(self)->None:
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=350, show=False, tag="connection_windows"):
        
            for field in ["host", "port", "name", "password"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    if field!="password":
                        dpg.add_input_text(default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")    
                    else:
                        dpg.add_input_text(default_value="", tag=f"connection_{field}", password=True)

            dpg.add_button(label="Connect", callback=self.run_chat)

    def run_chat(self, sender, app_data)->None:
        self._log.info("Starting initialization process")
        # recover parameter from windows
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")

        # derive the key
        salt = b'34Yh23FnfQxjOg=='
        kdf_ = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 16,
        salt = salt,
        iterations = 10000,
        )
        self._key = kdf_.derive(password.encode())
        self._log.debug(f"Derived key {self._key.hex()}")

        # hide connection window, show chat window
        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

        # start chat and register oneself
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        self._log.info(f"Connecting {name}@{host}:{port}")
        dpg.set_value("screen", "Connected - type a message and hit enter!")


    def encrypt(self, text:str)->bytes:
        # encrypt a text message
        gh = os.urandom(16)
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(gh))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(text.encode()) + padder.finalize()
        encrypted = encryptor.update(padded_plaintext) + encryptor.finalize()
        return gh, encrypted

    def decrypt(self, data:bytes)->str:
        # decrypt a text message
        gh = data[:16]
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(gh))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(data[16:]) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        return plaintext.decode()

    def send(self, text:str)->None:
        # encrypt and send the message
        if self._client is not None:
            gh, encrypted = self.encrypt(text)
            self._client.send_message(serpent.dumps({"data":encrypted, "encoding":"bytes"}))

    def recv(self)->None:
        # get the message and decrypt it
        if self._callback is not None:
            for user, message in self._callback.get():
                plaintext = self.decrypt(serpent.loads(message)["data"])
                self.update_text_screen(f"{user} : {plaintext}")
            self._callback.clear()


    def _create_chat_window(self)->None:
        # chat windows
        # known bug : the add_input_text do not display message in a user friendly way
        with dpg.window(label="Chat", pos=(0, 0), width=800, height=600, show=False, tag="chat_windows", on_close=self.on_close):
            dpg.add_input_text(default_value="Readonly\n\n\n\n\n\n\n\nfff", multiline=True, readonly=True, tag="screen", width=790, height=525)
            dpg.add_input_text(default_value="Dites bonjour ...", tag="input", on_enter=True, callback=self.text_callback, width=790)


    def _create_menu(self)->None:
        # menu (file->connect)
        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Connect", callback=self.connect)


    def create(self):
        # create the context and all windows
        dpg.create_context()

        self._create_chat_window()
        self._create_connection_window()
        self._create_menu()        
            
        dpg.create_viewport(title='Secure chat - or not', width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()


    def update_text_screen(self, new_text:str)->None:
        # from a nex_text, add a line to the dedicated screen text widget
        text_screen = dpg.get_value("screen")
        text_screen = text_screen + "\n" + new_text
        dpg.set_value("screen", text_screen)


    def text_callback(self, sender, app_data)->None:
        # every time a enter is pressed, the message is gattered from the input line
        text = dpg.get_value("input")
        self.update_text_screen(f"Me: {text}")
        self.send(text)
        dpg.set_value("input", "")


    def connect(self, sender, app_data)->None:
        # callback used by the menu to display connection windows
        dpg.show_item("connection_windows")

    def loop(self):
        # main loop
        while dpg.is_dearpygui_running():
            self.recv()
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

    def on_close(self):
        # called when the chat windows is closed
        self._client.stop()
        self._client = None
        self._callback = None



if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()

