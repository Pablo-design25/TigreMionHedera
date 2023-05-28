from hedera import (
    AccountId,
    Client,
    PrivateKey,
    PublicKey,
    TopicMessageSubmitTransaction
)
import mysql.connector
from hedera import TopicId

# Configura los parámetros de conexión a la base de datos MySQL
db_config = {
    'user': 'Hackaton',
    'password': 'Hackaton',
    'host': '127.0.0.1',
    'database': 'busschedule',
    'raise_on_warnings': True
}
# Configura la conexión a la red de Hedera
client = Client.forTestnet()  # Conexión a la red de prueba de Hedera
private_key = PrivateKey.fromString("302e020100300506032b6570042204209597d61b8b56b3630f3b71ae39a5f56c2665c16063190ea10a668bf98e8af275")
public_key = private_key.getPublicKey()
client.setOperator(AccountId.fromString("0.0.13702904"), private_key)

# Obtén los datos que deseas enviar a Hedera y guardar en MySQL
numPersons = 3
dates = '2023-05-15'
times = '09:30:00'
bus_id = 1
topic_id = TopicId.fromString("0.0.13703099")
datos = {"numPersons": numPersons,
         "dates": dates,
         "times": times,
         "bus_id": bus_id,
         }

try:
    # Crea la conexión a la base de datos MySQL
    db_connection = mysql.connector.connect(**db_config)
    
    # Verifica si la conexión se ha establecido correctamente
    if db_connection.is_connected():
        print("Conexión exitosa a la base de datos MySQL")

    # Resto del código para realizar operaciones en la base de datos
    # Envia el mensaje a Hedera
    transaction = TopicMessageSubmitTransaction() \
        .setTopicId(topic_id) \
        .setMessage(str(numPersons))\
        .setMessage(dates) \
        .setMessage(times)\
        .setMessage(str(bus_id)) \
        .execute(client) \
        .getReceipt(client)

    # Guarda los datos en MySQL
    cursor = db_connection.cursor()
    sql = "INSERT INTO flow (numPersons, times, dates, bus_id) VALUES (%s, %s, %s, %s)"
    values = (numPersons, times,dates,bus_id)
    cursor.execute(sql, values)
    db_connection.commit()

    
except mysql.connector.Error as error:
    print("Error al conectar a la base de datos MySQL:", error)
finally:
    # Cierra la conexión a la base de datos
    if 'db_connection' in locals() and db_connection.is_connected():
        db_connection.close()
        print("Conexión cerrada a la base de datos MySQL")
