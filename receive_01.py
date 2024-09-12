import logging
import pika
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define SSL context and load certificates
context = ssl.create_default_context(
    cafile="certs\ca_cert.pem"  # Path to your CA certificate
)
context.verify_mode = ssl.CERT_REQUIRED
context.load_cert_chain(
    "certs\client_cert.pem",    # Path to your client certificate
    "certs\client_key.pem"      # Path to your client private key
)

# Set SSL options
ssl_options = pika.SSLOptions(context)

# Define connection parameters for RabbitMQ
conn_params = pika.ConnectionParameters(
    host="localhost",           # RabbitMQ server host
    port=5671,                  # SSL/TLS port
    ssl_options=ssl_options
)

# Establish a connection and create a channel
with pika.BlockingConnection(conn_params) as connection:
    channel = connection.channel()

    # Declare the queue (create if not exists)
    channel.queue_declare(queue="foobar")

    # Callback function to handle received messages
    def callback(ch, method, properties, body):
        logging.info(f"Received message: {body.decode()}")

    # Set up the consumer to listen to the queue
    channel.basic_consume(queue="foobar", on_message_callback=callback, auto_ack=True)

    logging.info("Waiting for messages. To exit press CTRL+C")
    
    # Start consuming messages
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        logging.info("Exiting the consumer...")

