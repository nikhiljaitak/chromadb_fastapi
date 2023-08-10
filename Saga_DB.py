import py_api_saga
import json
class DatabaseSaga:
        
    def update_product_state(state):
        data=json.dumps({"state":state})
        return data
        
    def update_shipping_state(shipping_state):
    #function to update the state in shipping service.
        data=json.dumps({"state":shipping_state})
        return data
    
    def insert_into_postgres(self):
        try:
            # Simulate an error for demonstration purposes
            if self.data.get("simulate_error"):
                raise Exception("Error inserting into PostgreSQL")
            print("Inserted into PostgreSQL:", self.data)
        except Exception as e:
            print("Error in insert_into_postgres:", e)
            raise e  # Re-raise the exception to trigger compensating actions

    def compensate_postgres(self):
        print("Compensating PostgreSQL:", self.data)

    def insert_into_vector_db(self):
        print("Inserted into Vector DB:", self.data)

    def compensate_vector_db(self):
        print("Compensating Vector DB:", self.data)

    def execute(self):
        from py_api_saga.py_api_saga import SagaAssembler

        try:
            result = SagaAssembler.saga().operation((DatabaseSaga.update_product_state, 'sold_out'),(DatabaseSaga.update_product_state, 'in_stock')).operation((DatabaseSaga.update_shipping_state, 'ready_to_dispatch')).choreography_execute()
            print(result)
        except SagaAssembler.SagaException as exception:
             return str(exception.operation_error)

    data = {
        "project_id": 123,
        "task_id": 456,
        "category_id": 789
    }


db_saga = DatabaseSaga()
db_saga.execute()
