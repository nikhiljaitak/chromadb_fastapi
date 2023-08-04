from google.cloud import pubsub_v1
import os
from ChromaDBRepository import ChromaDBRepository
import json

chroma_obj = ChromaDBRepository("promptmanagement")

def callback(message):
    print(f"Received message: {message.data}")
    json_string = message.data.decode('utf-8')
    dictionary_data = json.loads(json_string)
    print("dictionary_type",type(dictionary_data))
    dictionary_data['unique_id']=f"p{dictionary_data['project_id']}f{dictionary_data['task_id']}"
    chroma_obj.add_prompt(dictionary_data['prompt'], dictionary_data['response1'], dictionary_data['response2'], dictionary_data['task'], dictionary_data['task_id'], dictionary_data['unique_id'], dictionary_data['category'], dictionary_data['project_id'], dictionary_data['status'])
    
    message.ack()

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
