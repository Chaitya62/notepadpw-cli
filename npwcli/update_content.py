import os
import logging


from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace



from npwcli.spider import Spider





class NotepadSocket(SocketIO):

    def __init__(self, url_key):

        self.socket_url = 'https://live.notepad.pw'
        self.port = 443
        self.url_key = url_key
        self.filepath = ''
        self.file_stamp = 0


        # self.io = SocketIO(self.socket_url, self.port, BaseNamespace)

        super().__init__(self.socket_url, self.port, BaseNamespace)

        # logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
        # logging.basicConfig()
        
     


    def join_room(self):
        self.emit('join_room', self.url_key)

    def publish(self, content):


        io_data = dict()

        io_data['name'] = self.url_key
        io_data['text'] = content
        io_data['cursor_location'] = len(content)-1

        self.emit('editing', io_data)

    
        
class Notepad:

    def __init__(self, url_key, live_update=False):

        self.url_key = url_key
        self.domain = "https://notepad.pw/"
        self.spider = Spider(self.domain+self.url_key)
        self.pad_key = self.spider.pad_key

        self.content = self.spider.content
        self.haspw = (self.spider.url_key == '' and self.spider.pad_key == '')

        self.io = None

        if live_update:
            self.io = NotepadSocket(self.url_key)
            self.io.join_room()


    def get_content_from_file_path(self, file_path):

        content = ''

        with open(file_path) as f:
            content = f.read()

        return content


    def is_file_content_changed(self):

        new_file_stamp = os.stat(self.filepath).st_mtime

        if(new_file_stamp != self.file_stamp):
            return True
        return False


    def save_to_file(self, filename, overwrite):

        with open(filename, 'w') as f:
            f.write(self.content)

        return


    def save_file(self, filepath, overwrite):

        file_content = self.get_content_from_file_path(filepath)

        self.filepath = filepath
        self.file_stamp = os.stat(filepath).st_mtime

        if(overwrite):
            self.content = file_content
        else:
            self.content += file_content


        if self.io:
            self.io.publish(self.content)


        data = dict()

        data['key'] = self.pad_key
        data['pad'] = self.content
        data['pw'] = ''
        data['url'] = self.url_key
        data['monospace'] = 0
        data['caret'] = 1

        self.spider.save(data)

        return

    def view_file(self):
        return self.content

np = None

if __name__ == '__main__':

    np = Notepad('chaityashah', True)