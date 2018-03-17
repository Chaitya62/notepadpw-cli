import re

from urllib import request
from urllib.request import Request
from urllib.parse import urlencode
from multiprocessing.dummy import Pool as ThreadPool

from brotli import decompress

from npwcli.utils import is_url, make_url



class Spider:

    def __init__(self,url, verbose=False):
        self.url = url
        self.domain = ''
        self.response = ''
        self.verbose = verbose
        self.content = ''

        self.get_domain()
        self.USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'

        self.save_url = 'https://notepad.pw/save'
        
        


        self.url_key = ""

        self.pad_key = ""
        self.visit()

        if(self.url_key != "" and self.pad_key != ""):
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

        return


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


    def save(self, data):


        encoded_data = urlencode(data).encode('utf-8')

        request_obj = Request(self.save_url, method="POST", data=encoded_data, headers={})

        request_obj = self.add_headers(request_obj)
        request_obj.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
        request_obj.add_header('origin', 'https://notepad.pw')

        response_obj = request.urlopen(request_obj)




if __name__ == '__main__':
    content = ""
    #url = input('Enter the url : ')
    url = "https://notepad.pw/chaityashah"
    spider = Spider(url)

    print(spider.url_key)
    print(spider.pad_key)



