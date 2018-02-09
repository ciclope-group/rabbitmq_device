import rabbitmq_device as rmq

sender = rmq.RabbitMQ_sender('weather')

msg_info = "Hace buen tiempo"
msg_critical= "Hace mal tiempo"

while True:
    c = input("Introducir 'c' para enviar mensaje critico, cualquier otra cosa para informativo")
    if c == 'c':
        msg = msg_critical
        sev = 'critical'
    else:
        msg = msg_info
        sev = 'info'
    sender.send_message(sev,msg)
