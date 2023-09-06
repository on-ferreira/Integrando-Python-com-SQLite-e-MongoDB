import pprint

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from credentials import password

uri = f"mongodb+srv://onferreira:{password}@cluster0.e2s1ofa.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.test
collection = db.test_collection
print(collection)

# single insert
account = {
    "name": "Fulano",
    "cpf": "12345678910",
    "address": "Rua um, numero um",
    "type": "Corrente",
    "ag": "0001",
    "num": "1",
    "balance": "100"
}

# Inserindo a primeira conta criada no banco de dados
accounts = db.accounts
# account_id = accounts.insert_one(account).inserted_id
# print(account_id)
# pprint.pp(db.accounts.find_one())

# bulk inserts
new_accounts = [{
    "name": "Beltrano",
    "cpf": "98765432100",
    "address": "Travessa da rua, complemento",
    "type": "Corrente",
    "ag": "0001",
    "num": "11",
    "balance": "1000"
},
    {
        "name": "Ciclano",
        "cpf": "58294812300",
        "address": "Avenida Nida km x",
        "type": "Poupança",
        "ag": "0001",
        "num": "15",
        "balance": "1500"
    }]

# Inserindo  várias contas de uma vez no banco de dados
# result = accounts.insert_many(new_accounts)
# print(result.inserted_ids)
# print("Recuperando a inserção do new_accounts")
# pprint.pprint(db.accounts.find_one({"name": "Beltrano"}))


# Recuperando todas as contas no db
for acc in accounts.find():
    pprint.pprint(acc)

print(f"Total de contas: {accounts.count_documents({})}")
total_fulano = accounts.count_documents({"name": "Fulano"})
print(f"Total de contas de Fulano: {total_fulano}")
total_corrente = accounts.count_documents({"type": "Corrente"})
print(f"Total de contas corrente: {total_corrente}")
