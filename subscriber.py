from google.cloud import pubsub_v1
import os
from ChromaDBRepository import ChromaDBRepository
import json

chroma_obj = ChromaDBRepository("promptmanagement")

def callback(message):
    print(f"Received message: {message.data}")
    message.ack()
    json_string = message.data.decode('utf-8')
    dictionary_data = json.loads(json_string)
    print("dictionary_type",type(dictionary_data))
    dictionary_data['unique_id']=f"p{dictionary_data['project_id']}f{dictionary_data['task_id']}"
    retrieved_object=None
    all_objects=None
    try:
        
        result = chroma_obj.add_prompt(dictionary_data['prompt'], dictionary_data['response1'], dictionary_data['response2'], dictionary_data['task'], dictionary_data['task_id'], dictionary_data['unique_id'], dictionary_data['category'], dictionary_data['project_id'], dictionary_data['status'])
    
        if result == "success":
            print("new prompt to be saved")
            retrieved_object=chroma_obj.get_by_unique_id(input_dictionary['unique_id'])
            all_objects=chroma_obj.get_all()
            status = input_dictionary['status']
            message="successfully saved into vdb"
        else:
            print(result)
            status="error"
            
    except Exception as e:
        status="error"
        print(f"An error occurred: {e}")
    print( {"message": message,"status":status,"retrieved":retrieved_object,"all objects":all_objects})
    

def subscribe_to_topic(project_id, subscription_name):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nikhiljaitak/Downloads/firstpro-21081989-32e38025cedc.json"

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...\n")

    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    project_id = "firstpro-21081989"
    subscription_name = "promptresponsechannel-sub"

    subscribe_to_topic(project_id, subscription_name)
