import json
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=["http://localhost:9200"])
index_name = "jobs"

mapping = {
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "company": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "description": {"type": "text"},
            "link": {"type": "text"},
            "salary": {"type": "text"},
            "duration": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "workday": {
                "type": "text",
                "fields":{
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "location": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
            "modality": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword"
                    }
                }
            },
        }
    }
}

def create_index():
    es.indices.create(index=index_name, body=mapping)
    print(f"Index '{index_name}' created successfully.")

if not es.indices.exists(index=index_name):
    create_index()
else:
    es.indices.delete(index=index_name)
    create_index()

with open('../jobs.json', 'r') as f:
    jobs = json.load(f)

for i, job in enumerate(jobs):
    doc_id = i + 1
    if not es.exists(index=index_name, id=doc_id):
        es.index(index=index_name, id=doc_id, body=job)
        print(f"Document {doc_id} inserted.")
