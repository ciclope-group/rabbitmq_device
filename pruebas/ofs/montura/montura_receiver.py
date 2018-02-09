''' Mockup de la montura. Imprimirá por pantalla los mensajes que reciba'''
import rabbitmq_device as rmq
def callback(severity,message):
    print("[{0}] {1}".format(severity,message))

subscription = rmq.Subscription('weather:info','weather:critical')
receiver = rmq.RabbitMQ_receiver(subscription, callback)

receiver.start_consuming()
