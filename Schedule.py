import os
import sys
import logging
import uuid
import time

from mesos.interface import Scheduler
from mesos.native import MesosSchedulerDriver
from mesos.interface import mesos_pb2

logging.basicConfig(level=logging.INFO)

def new_task(offer):
    task = mesos_pb2.TaskInfo()
    id = uuid.uuid4()
    task.task_id.value = str(id)
    task.slave_id.value = offer.slave_id.value
    task.name = "task {}".format(str(id))

    cpus = task.resources.add()
    cpus.name = "cpus"
    cpus.type = mesos_pb2.Value.SCALAR
    cpus.scalar.value = 1

    mem = task.resources.add()
    mem.name = "mem"
    mem.type = mesos_pb2.Value.SCALAR
    mem.scalar.value = 1

    return task


class MyScheduler(Scheduler):
	def __init__(self,executor):
		self.numbers=["1 2 3","4 5 6"]
		self.counter = 0
		self.finished_task=0
		self.executor = executor

	def registered(self, driver, framework_id, master_info):
		logging.info("Registered with framework id: {}".format(framework_id))

	def resourceOffers(self, driver, offers):
		logging.info("Recieved resource offers: {}".format([o.id.value for o in offers]))
		
		for offer in offers:
			if self.counter<len(self.numbers):
				task = new_task(offer)
				task.executor.MergeFrom(self.executor)
				task.data=self.numbers[self.counter]
				
				time.sleep(2)
				logging.info("Launching task {task},using offer {offer}.".format(task=task.task_id.value,offer=offer.id.value))
				tasks = [task]
				driver.launchTasks(offer.id, tasks)
				self.counter+=1
	def statusUpdate(self,driver,update):
		logging.info("task {task} status is {status}".format(task=update.task_id.value,status=mesos_pb2.TaskState.Name(update.state)))
		
		if update.state==mesos_pb2.TASK_FINISHED:
			self.finished_task+=1
			if self.finished_task==len(self.numbers):
				logging.info("all task has finished")
				driver.stop()

if __name__ == '__main__':
    # make us a framework
	framework = mesos_pb2.FrameworkInfo()
	framework.user = ""  # Have Mesos fill in the current user.
	framework.name = "hello-world"

	executor = mesos_pb2.ExecutorInfo()
	executor.executor_id.value="default"
	executor.command.value="python {}".format(os.path.abspath("./Executor.py"))
	executor.name="Test Executor(Python)"
	executor.source="python test"

	driver = MesosSchedulerDriver(
		MyScheduler(executor),
		framework,
		"127.0.0.1:5050"  # assumes running on the master
	)
	driver.run()
