from fastapi import FastAPI, Form
from pydantic import BaseModel, Field
import inspect
from ChromaDBRepository import ChromaDBRepository
import json
from app_enum import AppEnum

app = FastAPI()

chroma_obj = ChromaDBRepository("promptmanagement")

#chroma_obj=ChromaDBRepository()

@app.get("/oelabs/promptmanagement/databases/vectordb/health")
def root():
    return {"message": AppEnum.RUNNING_STATUS_MESSAGE.value}


class validate_request_body(BaseModel):
    prompt:  str = Field(min_length=5,   max_length=5000)
    response1: str = Field(min_length=5,   max_length=5000)
    response2: str = Field(min_length=5,   max_length=5000)
    task: str = Field(min_length=5,   max_length=500)
    task_id: str = Field(min_length=0,  max_length=50)
    #unique_id: str = Field(min_length=1, max_length=50)
    category: str = Field(min_length=0, max_length=50)
    project_id: str = Field(min_length=0, max_length=50)
    status: str = Field(min_length=0, max_length=50)
    
def get_output_dictionary(body):
    # creating composite key
    unique_id=f"p{body.project_id}f{body.task_id}"

    output_dict = {
        'prompt': body.prompt,
        'response1': body.response1,
        'response2': body.response2,
        'task': body.task,
        'task_id': body.task_id,
        'unique_id': unique_id,
        'category': body.category,
        'project_id': body.project_id,
        'status': body.status
}

    return output_dict

@app.post("/oelabs/promptmanagement/databases/vectordb")
async def process_form(body: validate_request_body):
    print(AppEnum.FUNCTION_CURRENT_PLACEHOLDER.value, inspect.currentframe().f_code.co_name)

    input_dictionary =get_output_dictionary(body)
    print(input_dictionary)
    print('collection name:  ',chroma_obj)
    retrieved_object=None
    all_objects=None
    try:
        
        chroma_obj.add_prompt(input_dictionary['prompt'], input_dictionary['response1'], input_dictionary['response2'], input_dictionary['task'], input_dictionary['task_id'], input_dictionary['unique_id'], input_dictionary['category'], input_dictionary['project_id'], input_dictionary['status'])
        retrieved_object=chroma_obj.get_by_unique_id(input_dictionary['unique_id'])
        all_objects=chroma_obj.get_all()
        status = input_dictionary['status']
        message="successfully saved into vdb"
    except Exception as e:
        message = f"An error occurred: {e}"
        status="error"
        print(f"An error occurred: {e}")
    return {"message": message,"status":status,"retrieved":retrieved_object,"all objects":all_objects}


