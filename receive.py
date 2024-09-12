import pika
import ssl

# Define SSL context
ssl_context = ssl.create_default_context(
    cafile="certs/ca_cert.pem",
    # certfile="certs/client_cert.pem",
    # keyfile="certs/client_key.pem"
)

ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.load_cert_chain("certs/client_cert.pem",
                        "certs/client_key.pem")

ssl_options = pika.SSLOptions(ssl_context, "localhost")

# Create connection parameters
connection_params = pika.ConnectionParameters(
    # host='localhost',
    port=5671,
    # ssl_options=pika.SSLOptions(context=ssl_context)
    ssl_options=ssl_options
)

# Establish connection
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='test_queue')

# Callback function to handle messages
def callback(ch, method, properties, body):
    print(f"Received {body}")

# Consume messages from the queue
channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
