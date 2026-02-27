# LAB-2-CAFE
# BrewLink - Coffee SQS Worker

Este proyecto implementa una arquitectura en la nube utilizando AWS (SQS, EC2 y RDS) para procesar órdenes de una cafetería sin perder peticiones durante picos de alta demanda.

## Descripción
El sistema extrae los pedidos de una cola de mensajería (SQS) mediante un servidor de procesamiento (EC2) y los almacena en una base de datos relacional (RDS PostgreSQL). Una vez guardado el registro con éxito, el mensaje se elimina de la cola para evitar órdenes duplicadas.

## Tecnologías y Servicios de AWS
* **Amazon SQS:** Cola de mensajes para recibir y retener los pedidos.
* **Amazon EC2:** Servidor donde se ejecuta el worker en Python.
* **Amazon RDS:** Base de datos PostgreSQL para almacenar el registro de pedidos.
* **Python 3:** Lenguaje principal (`boto3` para AWS y `psycopg2` para la base de datos).

## Requisitos
1. Python 3.9 o superior.
2. Permisos configurados para acceder a AWS SQS.
3. Base de datos PostgreSQL creada en Amazon RDS.

# Pasos para ejecutar

Abre tu terminal y ejecuta estos comandos en orden:

```bash
# 1. Crea y activa el entorno
python -m venv coffee-env
source coffee-env/bin/activate

# 2. Instala las librerías
pip install boto3 psycopg2-binary

# 3. Inicia el programa
python worker_sqs.py
