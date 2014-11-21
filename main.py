import tornado.ioloop
import tornado.web

import hashlib
import uuid
import json

from time import mktime
from datetime import datetime
from email.utils import formatdate

up_user = ''
up_password = ''

up_method = 'PUT'
up_host = 'v1.api.upyun.com'
up_path = '/bucket/'

up_base_url = "http://bucket.b0.upaiyun.com/%s"

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		content_md5 = self.get_argument('md5', '')
		content_len = self.get_argument('len', '')
		content_type = self.get_argument('type', '')

		stamp = mktime(datetime.now().timetuple())
		date  = formatdate(timeval = stamp, localtime = False, usegmt = True)
		filename = hashlib.md5(uuid.uuid1().hex).hexdigest()

		base_string = "%s&%s&%s&%s&%s" % (
			up_method,
			up_path + filename,
			date,
			content_len,
			hashlib.md5(up_password).hexdigest())
		signature = hashlib.md5(base_string).hexdigest()

		headers = {"Authorization": "UpYun %s:%s" % (up_user, signature),
			   "Content-Type": content_type,
			   "Content-MD5": content_md5,
			   "Date": date,
			   "Expect": ""}

		self.write(json.dumps({
			"headers": headers,
			"method":  up_method,
			"host":    up_host,
			"path":    up_path + filename,
			"url":     up_base_url % filename
		}))


application = tornado.web.Application([
	(r"/storage", MainHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
