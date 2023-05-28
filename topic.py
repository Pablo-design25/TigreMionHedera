from hedera import (
    AccountId,
    Client,
    PrivateKey,
    TopicCreateTransaction,
    Hbar
)

# Configura la conexión a la red de Hedera
client = Client.forTestnet()  # Conexión a la red de prueba de Hedera
private_key = PrivateKey.fromString("302e020100300506032b6570042204209597d61b8b56b3630f3b71ae39a5f56c2665c16063190ea10a668bf98e8af275")
public_key = private_key.getPublicKey()
client.setOperator(AccountId.fromString("0.0.13702904"), private_key)

# Crea una transacción para crear un tema
topic_transaction = (
    TopicCreateTransaction()
    .setTopicMemo("Mi tema de prueba")  # Memo/descripción opcional del tema
    .setSubmitKey(public_key)  # Clave pública asociada al tema
    .setMaxTransactionFee(Hbar(100000))  # Tarifa máxima de la transacción en formato de tinybars (ajustar según tus necesidades)
)

# Ejecuta la transacción y obtén el ID de la transacción
transaction_id = topic_transaction.execute(client)

# Espera a que se complete la transacción
receipt = transaction_id.getReceipt(client)

# Obtener el ID de transacción
transaction_id_str = transaction_id.transactionId.toString()
print("ID de transacción:", transaction_id_str)

# Imprime el Topic ID del tema creado
topic_id = receipt.topicId
print("Topic ID:", topic_id.toString())





