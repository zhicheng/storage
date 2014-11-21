import urllib
import urllib2

import sys
import json
import hashlib

import json_hook	# convert json.loads unicode to ascii

fd = open(sys.argv[1])
data = fd.read()

# get storage parameters
query = {'len': str(len(data)),
	 'type': 'image/jpeg',
	 'md5': hashlib.md5(data).hexdigest()}
url = 'http://127.0.0.1:8888/storage?%s' % urllib.urlencode(query)
print url
request = urllib2.Request(url)
response = urllib2.urlopen(request)
params = json.loads(response.read(), object_hook=json_hook._decode_dict)

print params

url = "http://%s%s" % (params['host'], params['path'])
print url

opener = urllib2.build_opener(urllib2.HTTPHandler)
request = urllib2.Request(url, data, headers = params['headers'])
request.get_method = lambda: params['method'].encode("utf8")
response = opener.open(request)
print params['url']

