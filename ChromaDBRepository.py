
import chromadb


class ChromaDBRepository:
    def __init__(self, collection_name):
        self.collection_name = collection_name
        self.collection = self.create_vector_db()

    def create_vector_db(self):
        client = chromadb.Client()
        collection = client.create_collection(self.collection_name)
        return collection

    def add_prompt(self, prompt, project_name, task_id, unique_id, category):
        self.collection.add(
            documents=[prompt],
            metadatas=[
                { "project_name": project_name,"task_id":task_id,"category": category}
            ],
            ids=[unique_id]
        )
        print("prompt added successfully")  
         
    def get_all(self):
        return self.collection.get()

