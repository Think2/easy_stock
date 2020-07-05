import urllib.request
import urllib.parse

headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

dict = {
    'test':'hello word'
}

data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
request = urllib.request.Request("http://httpbin.org/post", data=data, headers=headers)
response = urllib.request.urlopen(request)

print(response.read().decode('utf-8'))
