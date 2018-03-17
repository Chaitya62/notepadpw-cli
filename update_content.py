from socketIO_client import SocketIO, LoggingNamespace
import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()


class NotepadSocket(SocketIO):

    def __init__(self, url_key):
        self.socket_url = 'https://live.notepad.pw'
        self.port = 443
        self.url_key = url_key

        self.io = SocketIO(self.socket_url, self.port, LoggingNamespace)
     


    def emit_eve(self, event, data):
    	self.io.emit(event, data)
        
