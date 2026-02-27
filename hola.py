import boto3
import psycopg2
import time

# configuracion de conexion
REGION = 'us-east-1'
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/568326961120/coffee-orders-queue'

DB_HOST = 'coffee-db.ci2b5o1xaj9z.us-east-1.rds.amazonaws.com'
DB_NAME = 'coffeeshop'
DB_USER = 'postgres'
DB_PASS = 'admin12345'


def procesar_pedidos():
    # cliente sqs
    sqs = boto3.client('sqs', region_name=REGION)
    print("Iniciando worker... esperando pedidos de cafe")

    while True:
        try:
            # buscar mensajes en la cola
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=10
            )

            if 'Messages' in response:
                for msg in response['Messages']:
                    body = msg['Body']
                    receipt_handle = msg['ReceiptHandle']

                    print(f"Pedido recibido: {body}")

                    # separo el string: Cafe|Fecha
                    cafe, fecha = body.split('|')

                    # conectar a rds
                    conexion = psycopg2.connect(
                        host=DB_HOST,
                        database=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS
                    )
                    cursor = conexion.cursor()

                    # insertar datos
                    query = "INSERT INTO coffee_orders (timestamp, coffee_type) VALUES (%s, %s)"
                    cursor.execute(query, (fecha, cafe))

                    conexion.commit()
                    cursor.close()
                    conexion.close()

                    # borrar mensaje para que no se duplique la orden
                    sqs.delete_message(
                        QueueUrl=QUEUE_URL,
                        ReceiptHandle=receipt_handle
                    )
                    print("Orden guardada en base de datos y eliminada de la cola")

        except ValueError:
            print("Formato de mensaje incorrecto")
        except Exception as e:
            print(f"Error detectado: {e}")
            time.sleep(5)


if __name__ == '__main__':
    procesar_pedidos()