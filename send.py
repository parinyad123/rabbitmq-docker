import pika
import ssl

# Define SSL context
# ssl_context = ssl.create_default_context(
#     cafile="certs/ca_cert.pem",
#     certfile="certs/client_cert.pem"
#     # keyfile="certs/client_key.pem"
# )

ssl_context = ssl.create_default_context(
    cafile="certs\ca_cert.pem"  # Path to your CA certificate
)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.load_cert_chain(
    "certs\client_cert.pem",    # Path to your client certificate
    "certs\client_key.pem"      # Path to your client private key
)

# Set SSL options
ssl_options = pika.SSLOptions(ssl_context)


ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create connection parameters
connection_params = pika.ConnectionParameters(
    host='localhost',
    port=5671,
    ssl_options=pika.SSLOptions(context=ssl_context)
)

# Establish connection
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='test_queue')

# Send a message
channel.basic_publish(exchange='', routing_key='test_queue', body='Hello, RabbitMQ!')
print("Message sent successfully")

# Close the connection
connection.close()

