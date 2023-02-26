# https://superfastpython.com/thread-queue-task-done-join/

# EXAMPLE 1

# example of join and task done for a thread queue
from time import sleep
from random import random
from queue import Queue
from threading import Thread
 
# task for the producer thread
def producer(queue):
    print('Producer starting')
    # add tasks to the queue
    for i in range(10):
        # generate a task
        task = (i, random())
        print(f'.producer added {task}')
        # add it to the queue
        queue.put(task)
    # send a signal that no further tasks are coming
    queue.put(None)
    print('Producer finished')
 
# task for the consumer thread
def consumer(queue):
    print('Consumer starting')
    # process items from the queue
    while True:
        # get a task from the queue
        task = queue.get()
        # check for signal that we are done
        if task is None:
            break
        # process the item
        sleep(task[1])
        print(f'.consumer got {task}')
        # mark the unit of work as processed
        queue.task_done()
    # mark the signal as processed
    queue.task_done()
    print('Consumer finished')

# # create the shared queue
# queue = Queue()
# # create and start the producer thread
# producer = Thread(target = producer, args = (queue, ))
# producer.start()
# # create and start the consumer thread
# consumer = Thread(target = consumer, args = (queue, ))
# consumer.start()
# # wait for the producer to finish
# producer.join()
# print('main found that the producer has finished')
# # wait for the queue to empty
# queue.join()
# print('main found that all tasks are processed')

# EXAMPLE 2

q = Queue()

def worker():
    while True:
        item = q.get()
        print(f'Working on {item}')
        print(f'Finished {item}')
        q.task_done()

# turn-on the worker thread
Thread(target = worker, daemon = True).start()

# send thirty task requests to the worker
for item in range(30):
    q.put(item)

# block until all tasks are done
q.join()