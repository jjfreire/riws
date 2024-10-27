from elasticsearch import Elasticsearch

#Conexión local Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"])

#Nombre índice
index_name = "trabajos"

#Mapeo de campos (estructura de documentos)
mapping = {
        "mappings": {
            "properties": {
                "title" : {"type": "text"},
                "company" : {"type": "text"},
                "description" : {"type": "text"},
                "link" : {"type": "text"},
                "salary" : {"type": "text"},
                "duration" : {"type": "text"},
                "workday" : {"type": "text"},
                "location" : {"type": "text"},
                "modality" : {"type": "text"}
            }
        }
}

#Crear índice
es.indices.create(index=index_name, body=mapping)
print(f"Índice '{index_name}' creado con éxito.")