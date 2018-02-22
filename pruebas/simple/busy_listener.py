import rabbitmq_device as rmq
import time,threading

class rmq_listener(threading.Thread):
    def run(self):
        
        def callback(s,m):
            print("[{0}] {1}".format(s,m))

        s = rmq.Subscription("sender:sender")

        listener = rmq.RabbitMQ_receiver(s,callback)

        listener.start_consuming()

l = rmq_listener()
l.start()
i=0
while True:
    i +=1
    print(i)
    time.sleep(2)
