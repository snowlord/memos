#coding:utf-8

###the file for tesing framework 

import logging

import tornado.ioloop
import tornado.httpserver
import tornado.web

log = logging.getLogger(__file__)
fileHandler = logging.FileHandler("log.txt")
log.addHandler(fileHandler)
log.setLevel(logging.INFO)

class MainHandler(tornado.web.RequestHandler):
	def get(self):
		numbers = self.get_argument("numbers")
		sum = self.get_argument("sum")
		#self.write("from: " + self.request.remote_ip)
		#self.write("\r\n")
		#self.write("hello,world!")
		
		log.info("from: " + self.request.remote_ip)
		log.info("numbers: "+numbers)
		log.info("sum: "+sum)
		pass


def main():
	handlers=[(r'/',MainHandler)]
	app = tornado.web.Application(handlers)
	server = tornado.httpserver.HTTPServer(app)
	server.listen(8080)
	tornado.ioloop.IOLoop.current().start()


if __name__=="__main__":
	main()
