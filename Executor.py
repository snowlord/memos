#coding:utf-8

import time
import sys
import threading

import urllib
import urllib2

from mesos.native import MesosExecutorDriver
from mesos.interface import Executor
from mesos.interface import mesos_pb2

### this part like slave task

header={"UserAgent":"Mozilla/5.0"}

class MyExecutor(Executor):

	def __init__(self):
		pass

	def launchTask(self,driver,task):
		
		def runtask():
			update = mesos_pb2.TaskStatus()
			update.task_id.value = task.task_id.value
			update.state=mesos_pb2.TASK_RUNNING
			driver.sendStatusUpdate(update)

			data = task.data

			query_arg = {'numbers':data,'sum':sum([int(d) for d in data.split(" ")])}
			encode_arg = urllib.urlencode(query_arg)
			main_url="http://127.0.0.1:3000/results?{param}".format(param=encode_arg)

			print urllib2.urlopen(urllib2.Request(main_url,headers=header)).read()

			

			update = mesos_pb2.TaskStatus()
			update.task_id.value = task.task_id.value
			update.state=mesos_pb2.TASK_FINISHED
			driver.sendStatusUpdate(update)
			pass

		thread = threading.Thread(target=runtask)
		thread.start()
		pass



if __name__=="__main__":
	print "start executor"
	driver = MesosExecutorDriver(MyExecutor())
	sys.exit(0 if driver.run()==mesos_pb2.DRIVER_STOPPED else 1)
