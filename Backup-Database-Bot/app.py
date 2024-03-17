from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime


'''
Script che fa un backup giornaliero del database
'''
load_dotenv('.env')



client_origin = MongoClient(f'mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@{os.getenv("MONGO_HOST")}:{os.getenv("MONGO_PORT")}/')

client_destination = MongoClient(f'mongodb://{os.getenv("MONGO_USER_BACKUP")}:{os.getenv("MONGO_PASSWORD_BACKUP")}@{os.getenv("MONGO_HOST_BACKUP")}:{os.getenv("MONGO_PORT_BACKUP")}/')






db_origin = client_origin['users']
db_destination = client_destination['users']

def backup_data(origin_db, destination_db):
    # Ottieni tutte le raccolte dal database di origine
    collections = db_origin.list_collection_names()
    
    # Per ogni raccolta, fai il backup dei documenti
    for collection_name in collections:
        # Ottieni la raccolta dal database di origine
        collection = origin_db[collection_name]
        
        # Ottieni tutti i documenti dalla raccolta di origine
        documents = collection.find({})
        
        # Inserisci i documenti nella raccolta di destinazione
        for document in documents:
            destination_db[collection_name].insert_one(document)

# Esegui la funzione di backup
backup_data(db_origin, db_destination)
with open ('backup_list.txt', 'a') as file:
    file.write(f"backup eseguito il {datetime.now()} \n")