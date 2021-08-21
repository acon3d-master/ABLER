import urllib.parse

def encode(text):
    return urllib.parse.quote(text, safe='')\
        .replace('-', '%2d').replace('.', '%2e').replace('_', '%5f')\
        .replace('%', '_')

def decode(underscore_encoded):
    return urllib.parse.unquote(underscore_encoded.replace('_','%'), errors='strict')