#
# Start Rabbit MQ Server in Docker.
#
# Expose ports:
#   5671 --> 5671, 5672 --> 5672 (used by AMQP 0-9-1 and 1.0 clients without and with TLS)
#   8080 --> 15672 (Management Plugin)
#
# Learn more: https://hub.docker.com/_/rabbitmq/


docker run --hostname my-rabbit --rm --name some-rabbit -p 5672:5672 -p 5671:5671 -p 8080:15672 rabbitmq:3