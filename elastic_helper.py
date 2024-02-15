import os
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from config import get_environment_config
from helper import split_and_format_data
from langchain_openai import OpenAIEmbeddings

# Elasticsearch settings
elastic_conn_str = get_environment_config('ELASTIC_CONNECTION_URL')
embedding_func = OpenAIEmbeddings(
                openai_api_key=get_environment_config('OPEN_API_KEY'),
            )


def get_subfolders(folder_path):
    subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
    return subfolders

def get_files_in_folder(folder_path):
    files = [f.path for f in os.scandir(folder_path) if f.is_file()]
    return files

class Elastic_Retrival:
    def __init__(self, connection_string):
        self.es = Elasticsearch(connection_string)

    def create_index(self, index_name):
        index_settings = {
            "mappings": {
                "properties": {
                    "meta": {
                        "type": "object"
                    },
                    "content": {
                        "type": "text"
                    },
                    "vector": {
                        "type": "dense_vector",
                        "dims": 1536
                    }
                }
            }
        }
        try:
            self.es.indices.create(index=index_name, body=index_settings)
            print(f"Index '{index_name}' created successfully.")
        except Exception as e:
            print(str(e))
            if "resource_already_exists_exception" in str(e):
                print(f"Index '{index_name}' already exists.")

    def index_pdf(self, path, index):
        self.create_index(index_name=index)
        docs = split_and_format_data(path=path)
        for doc in docs:
            doc['vector'] = embedding_func.embed_query(str(doc['content']))
            self.index_documents_with_metadata(index_name=index, documents=[doc])

       

    def index_documents_with_metadata(self, index_name, documents):
        actions = [
            {
                '_op_type': 'index',
                '_index': index_name,
                '_source': {
                    'meta': document['meta'],
                    'content': document['content'],
                    'vector': document.get('vector', []) 
                }
            }
            for document in documents
        ]

        bulk(self.es, actions)

    def search_similar_documents(self, query_vector, index_name, top_k=2, min_score=0.4):
        query = {
            "query": {
                "bool": {
                    "must": {
                        "script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {"query_vector": query_vector}
                            }
                        }
                    },
                    "filter": {
                        "range": {
                            "_score": {"gte": min_score}
                        }
                    }
                }
            },
            "size": top_k,
            "_source": ["meta", "content"]
        }

        result = self.es.search(index=index_name, body=query)

        similar_results = [
            {
                'document_id': hit['_id'],
                'score': hit['_score'],
                'meta': hit['_source']['meta'],
                'content': hit['_source']['content']
            }
            for hit in result['hits']['hits']
        ]

        # Sort the results by score in descending order
        similar_results = sorted(similar_results, key=lambda x: x['score'], reverse=True)

        return similar_results[:top_k]



#index the docs to the elasticsearch 
def index_documents():
    es = Elastic_Retrival(connection_string=elastic_conn_str)

    indices = get_subfolders("./documents")
    for index in indices:
        documents_paths = get_files_in_folder(f"./documents/{index}")
        print(documents_paths)
        for doc_path in documents_paths:
            new_index = doc_path.split("/")[2]
            es.index_pdf(path=doc_path,index=new_index)


def indices():
    indices = get_subfolders("./documents")
    return indices


def get_elastic_retrival_obj():
    return Elastic_Retrival(connection_string=elastic_conn_str)