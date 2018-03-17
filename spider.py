import re

from http.cookiejar import MozillaCookieJar
from urllib import request
from urllib.request import Request
from urllib.parse import urlencode
from multiprocessing.dummy import Pool as ThreadPool

from brotli import decompress

from utils import is_url, make_url
from update_content import NotepadSocket



class Spider:

    def __init__(self,url, verbose=False):
        self.url = url
        self.domain = ''
        self.response = ''
        self.verbose = verbose
        self.get_domain()
        self.USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
        if(self.verbose):
            print("Visiting domain : " + self.domain)
        self.urls = []
        self.save_url = 'https://notepad.pw/save'
        self.io = None
        
        


        self.url_key = ""

        self.pad_key = ""
        self.headers  = None
        self.cookiejar = MozillaCookieJar()
        self.opener = request.build_opener(request.HTTPCookieProcessor(self.cookiejar))
        self.opener.addheaders = []
        self.opener.addheaders.append(('User-Agent', self.USER_AGENT))
        request.install_opener(self.opener)
        self.visit()

        if(self.url_key != "" and self.pad_key != ""):
            #self.io = NotepadSocket(self.url_key)
            #self.io.emit_eve('join_room', self.url_key)

            self.hit("https://notepad.pw/fetch/"+self.url_key+"/?_=153264234352")

       
    
    def get_domain(self):

        pattern = r'(http[s]?://[a-zA-Z0-9]+?\.?[a-zA-Z0-9\-]+\.[a-z]{2,})'
        result = re.findall(pattern, self.url)

        if(result):
            self.domain = result[0]

    def visit(self):
            
            if(self.verbose):
                print("Visiting {}".format(self.url))
            
            try:
                request_obj = Request(self.url)
                request_obj.add_header('User-Agent',self.USER_AGENT)
                request_obj.add_header('Content-Type', 'text/html')
                response_obj = request.urlopen(request_obj)
                self.headers = response_obj.getheaders()
                self.cookies = response_obj.getheader('Set-Cookie')
                self.response = response_obj.read().decode('utf-8');
                self.find_urls(self.response)
                
                self.get_pad_key(self.response)
                self.get_url_key(self.response)

            except Exception as e: 
                print(e)
        
            #print(self.urls)


    def add_headers(self, request_obj):

        request_obj.add_header('User-Agent',self.USER_AGENT)
        request_obj.add_header('Cookie', self.cookies)
        request_obj.add_header('referer', 'https://notepad.pw/'+self.url_key)
        request_obj.add_header('x-requested-with', 'XMLHttpRequest')
        request_obj.add_header('accept-encoding', 'gzip, deflate, br')
        
        return request_obj



    def hit(self, url):

        request_obj = Request(url)
        request_obj = self.add_headers(request_obj)

        response_obj = request.urlopen(request_obj)
        self.cookies = response_obj.getheader('Set-Cookie')
        self.content = decompress(response_obj.read()).decode('utf-8')
        self.fetch_resp = response_obj

        return


    


    def find_urls(self, response):

        url_find_pattern = r'<a href="?\'?([^"\'>]*)'
        results = re.findall(url_find_pattern, response)

        if(results):
            
            for url in results:
                if is_url(url):
                    self.urls.append(url)
                else: 
                    self.urls.append(make_url(self.domain, url))



    def get_pad_key(self, response):

        pad_key_pattern = r'(?<=pad_key = \')[a-z0-9]+'
        results = re.findall(pad_key_pattern, response)

        if(results):

            for pad_key in results:
                self.pad_key = pad_key

    def get_url_key(self, response):

        url_key_pattern = r'(?<=url_key = \')[a-z0-9]+'
        results = re.findall(url_key_pattern, response)

        if(results):

            for url_key in results:
                if(url_key):
                    self.url_key = url_key


    def get_content_from_file_path(self, file_path):

        content = ''

        with open(file_path) as f:
            content = f.read()

        return content

    def save(self, file_path, overwrite):



        content = self.get_content_from_file_path(file_path)

        if not overwrite:
            content = self.content + content

        if(self.io):
            io_data = dict()

            io_data['name'] = self.url_key
            io_data['text'] = content
            io_data['cursor_location'] = len(content)-1

            self.io.emit_eve('editing', io_data)
        #self.io.emit_eve('update', io_data)



        t = 100000
        while t > 0:
            t-=1

        data = dict()

        data['key'] = self.pad_key
        data['pad'] = content
        data['pw'] = ''
        data['url'] = self.url_key
        data['monospace'] = 0
        data['caret'] = 1

        # print(data)

        encoded_data = urlencode(data).encode('utf-8')


        request_obj = Request(self.save_url, method="POST", data=encoded_data, headers={})


        # set headers 
        request_obj = self.add_headers(request_obj)
        request_obj.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        request_obj.add_header('origin', 'https://notepad.pw')

        self.request_obj = request_obj
       

        
        response_obj = request.urlopen(request_obj)

        self.save_response = response_obj



if __name__ == '__main__':
    content = ""
    url = input('Enter the url : ')
    #url = "https://notepad.pw/chaityashah"
    spider = Spider(url)

    print(spider.url_key)
    print(spider.pad_key)



