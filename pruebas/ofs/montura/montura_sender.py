# coding = utf-8
"""Mockup de la montura. Se moverá 10 grados y lo notificará cada vez que se pulse Enter"""
import rabbitmq_device as rmq

sender = rmq.RabbitMQ_sender('montura')
pos = 0

while True:
    sender.send_message('info','GOTO {}'.format(pos))
    pos += 10
    input('Pulsar ENTER para mover otra vez')
