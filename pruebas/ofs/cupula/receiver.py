import rabbitmq_device as rmq

def callback(severity,message):
    if message[:3] == "GOTO"[:3]:
        goto = message.split(" ")[1]
        print("Voy hacia {}".format(goto))
    else:
        print("[{0}] {1}".format(severity,message))

subscription = rmq.Subscription('montura:info','weather:critical')
receiver = rmq.RabbitMQ_receiver(subscription,'localhost',callback)
receiver.start_consuming()
