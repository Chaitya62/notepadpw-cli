import re

def is_url(url):
	url_pattern = r'^https?://(.*?)\.(.*?)$'
	result = re.findall(url_pattern, url)

	if len(result) is 0: 
		return False
	return True

def make_url(url, ext):
	if ext[0] is '/':
		return url + ext
	else:
		return url + '/' + ext
