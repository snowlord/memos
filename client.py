#coding:utf-8



import urllib
import urllib2


header={"UserAgent":"Mozilla/5.0"}

def requestURL():
	data="1 2 3"
	query_arg = {'numbers':data,'sum':sum([int(d) for d in data.split(" ")])}
	encode_arg = urllib.urlencode(query_arg)

	main_url="http://192.168.12.179:8080/?{param}".format(param=encode_arg)

	print(urllib2.urlopen(urllib2.Request(main_url,headers=header)).read())

if __name__=="__main__":
	requestURL()

