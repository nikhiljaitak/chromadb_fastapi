
import chromadb
from chromadb.utils import embedding_functions


class ChromaDBRepository:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.collection = self.create_vector_db()

    def create_vector_db(self):
        client = chromadb.PersistentClient(path="chromadb_store")
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        collection = client.get_or_create_collection(self.collection_name,metadata={"hnsw:space": "cosine"},embedding_function=sentence_transformer_ef)
        return collection

    def add_prompt(self, prompt, response1, response2, task , task_id, unique_id, category, project_id, status):
        
            print(len(self.collection.get(ids=[unique_id])['ids']))
            if len(self.collection.get(ids=[unique_id])['ids']) >0:
                exception_message=f"Prompt already exists having unique_id:{unique_id}"
                raise Exception(exception_message)
            
            print("prompt doesnt exist")
            self.collection.add(
                documents=[prompt],
                metadatas=[
                    { "response1": response1,"response2": response2,"task":task,"task_id":task_id,"unique_id":unique_id, "category":category,"project_id": project_id,"status":status}
                ],
                ids=[unique_id]
            )
            print("prompt added successfully")  
         
    def get_by_unique_id(self, unique_id):
        return self.collection.get(include=['embeddings', 'documents', 'metadatas'], ids=[unique_id])
    
    def get_all(self):
        return self.collection.get()

