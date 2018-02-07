#!/bin/python
# coding: utf-8

import config
import pika
class RabbitMQ_sender:
    '''Clase de un dispositivo que enviará mensajes a un exchange de RabbitMQ con su nombre'''
    def __init__(self,my_name,server_ip="localhost"):
        '''Inicialización. Parámetros:
    my_name: string    Nombre del dispositivo. Se corresponde con el nombre del exchange al que va a publicar
    server_ip: string  Dirección IP del servidor de RabbitMQ (Opcional, 'localhost' por omisión).
    '''
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=server_ip))
        self.channel = self.connection.channel()
        self.my_name=my_name
        
        # Declarar el exchage al que se va a publicar
        channel.exchange_declare(exchange=my_name,
                    exchange_type="direct")

    def send_message(severity,message):
        '''Envía un mensaje. Parámetros:
    severity: 'info' | 'critical'  Importancia del mensaje
    message: Cualquier cosa        Cuerpo del mensaje

Tener en cuenta que si se pasa una string, se recibirá un objeto bytes
'''
        self.channel.basic_publish(exchange=self.my_name,
                routing_key=severity,
                body=message)
    def __del__(self):
        self.connection.close()

class RabbitMQ_receiver:
    'Clase de un dispositivo que recibirá mensajes de RabbitMQ'
    def __init__(self,subscription,ip_server,callback):
        '''Inicialización. Parámetros:
    subscription:   lista de diccionarios de la forma {"queue":q,"severity":s}
                    donde q es una string que corresponde al nombre de un
                    dispositivo del que se quiere leer y s es una string que
                    corresponde al tipo de mensajes que se quiere recibir en
                    función de su importancia
    
    ip_server:  string      Dirección IP del servidor de RabbitMQ
    
    callback:   Funcion(severity,message) que se ejecutará cada vez que llegue
                un mensaje. El parametro severity contendrá la importancia y
                el parametro message, el cuerpo del mensaje.
'''
        self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=ip_server))
        self.channel = self.connection.channel()
        self.callback = callback

        if subscription:
            self.name=self.channel.queue_declare(exclusive=True).method.queue
            for s in config.subscription:

                # Declarar el exchange del que se quiere recibir, por si se
                # ejecuta antes que el emisor correspondiente
                channel.exchange_declare(exchange=s['queue'],
                        exchange_type="direct")

                # Avisar de que se quiere escuchar del exchange correspondiente
                self.channel.queue_bind(exchange=s['queue'],
                        queue=self.name,
                        routing_key=s['severity'])
    def start_consuming(self):
        def callback(ch,method,properties,body):
            return self.callback(method.roting_key,body)

        self.channel.basic_consume(callback,
                queue=self.name,
                no_ack=True)
        print("[x] Iniciado el consumo en {}".format(config.my_name))
        self.channel.start_consuming()
    def __del__(self):
        self.connection.close()
