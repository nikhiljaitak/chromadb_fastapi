from fastapi import FastAPI, Form
from pydantic import BaseModel, Field
import inspect
from ChromaDBRepository import ChromaDBRepository
import json
from app_enum import AppEnum

app = FastAPI()

chroma_obj = ChromaDBRepository("oelabs_promptmanagement")

#chroma_obj=ChromaDBRepository()

@app.get("/oelabs/promptmanagement/databases/vectordb/health")
def root():
    return {"message": AppEnum.RUNNING_STATUS_MESSAGE.value}


class validate_request_body(BaseModel):
    prompt:  str = Field(min_length=5,   max_length=5000)
    task_id: str = Field(min_length=0,  max_length=2000)
    unique_id: str = Field(min_length=1, max_length=50)
    category: str = Field(min_length=0, max_length=50)
    project_name: str = Field(min_length=0, max_length=50)
    
def get_output_dictionary(body):
    
    prompt = body.prompt
    task_id = body.task_id
    unique_id = body.unique_id
    category=body.category
    project_name=body.project_name


    output_dict = {
        'prompt': prompt,
        'project_name':project_name,
        'task_id': task_id,
        'unique_id': unique_id,
        'category':category
    }

    return output_dict


@app.post("/oelabs/promptmanagement/databases/vectordb/")
async def process_form(body: validate_request_body):
    print(AppEnum.FUNCTION_CURRENT_PLACEHOLDER.value, inspect.currentframe().f_code.co_name)

    input_dictionary =get_output_dictionary(body)
    print(input_dictionary)
    print('collection name:  ',chroma_obj)
    
    output= chroma_obj.add_prompt(input_dictionary['prompt'], input_dictionary['project_name'], input_dictionary['task_id'], input_dictionary['unique_id'], input_dictionary['category'])
    alladded=chroma_obj.get_all()
    return {"message": "Form values processed successfully","yes":alladded}
