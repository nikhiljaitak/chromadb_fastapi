from google.cloud import pubsub_v1

def publish_message(project_id, topic_name, message_data):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nikhiljaitak/Downloads/firstpro-21081989-32e38025cedc.json"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_name)

    message_bytes = message_data.encode("utf-8")
    future = publisher.publish(topic_path, data=message_bytes)
    message_id = future.result()

    print(f"Published message: {message_data}, Message ID: {message_id}")
    
data = [
    {
        "prompt": "design for a er diagram",
        "response1": "Test text",
        "response2": "text test",
        "task": "Design wireframes or mockups to visualize the layout and user interface",
        "status": "Completed",
        "project_id": "1",
        "task_id": "3",
        "category":"design"
}
,
    {
        "prompt": "create sdlc best practices",
        "response1": "Test text",
        "response2": "text test",
        "task": "best practices",
        "status": "Completed",
        "project_id": "1",
        "task_id": "4",
        "category": "design"
    }
]


if __name__ == "__main__":
    project_id = "firstpro-21081989"
    topic_name = "promptresponsechannel"
    import json
    import os
    for dictionary in data:
        message_data_json = json.dumps(dictionary)
        print(type(message_data_json))
        publish_message(project_id, topic_name, message_data_json)
    message_data = "Hello, Pub/Sub!"

    #publish_message(project_id, topic_name, message_data)
