from threading import Thread
import time

# WITHOUT DAEMON
def sleeper(n, name):
    print('{} going to sleep 3 seconds \n'.format(name))
    time.sleep(n)
    print('{} has woke up \n'.format(name))

# start = time.time()

# with thread
thread_list = []
for i in range(5):
    t = Thread(target = sleeper, name = 'thread {}'.format(i), args = (5, 'thread {}'.format(i)))
    thread_list.append(t)
    t.start()

for t in thread_list:
    t.join()

# without thread
# for i in range(5):
#     sleeper(3, 'thread {}'.format(i))

# print('FINISH ALL THREAD = {}'.format(time.time() - start))

# WITH DAEMON
# total = 4

# def func_1():
#     global total
#     for i in range(10):
#         time.sleep(2)
#         total += 1
#         print('total func_1 = {}'.format(total))
#     print('func_1 done')

# def func_2():
#     global total
#     for i in range(7):
#         time.sleep(1)
#         total += 1
#         print('total func_2 = {}'.format(total))
#     print('func_2 done')

# def func_3():
#     global total
#     while True:
#         if total > 5:
#             print('overload')
#             total -= 3
#             print('total func_3 = {}'.format(total))
#         else:
#             time.sleep(1)
#             print('waiting')

# t_1 = Thread(target = func_1)
# t_2 = Thread(target = func_2)
# t_3 = Thread(target = func_3, daemon = True)

# t_1.start()
# t_2.start()
# t_3.start()

# t_1.join()
# t_2.join()
# # t_3.join()

# # (t_3.join di-on-in) OR (daemon t_3 = False) OR ((t_3.join di-on-in) AND (daemon t_3 = True)) :
# # trus looping sampai task 3 selesai, kl ga selesai-selesai ya ga mati-mati programnya
# # daemon = bayangan dari main thread
# the join method is used to wait for each thread to complete before moving on to the next line of code