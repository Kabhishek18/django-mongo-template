from pymongo import MongoClient
import environ
from django.conf import settings

env = environ.Env(DEBUG=(bool, False))

class MongoDBConnection:
    def __init__(self, db_name=None):
        self.client = MongoClient(env.get_value('MONGO_DB'))
        self.db_name = db_name or settings.DATABASES['default']['NAME']  # Use the default database name

    def get_db(self, db_name=None):
        return self.client[db_name or self.db_name]

    def close(self):
        self.client.close()

class MongoDBUtility:
    def __init__(self, db_name=None):
        self.db_name = db_name or settings.DATABASES['default']['NAME']  # Use the default database name
        self.mongo_conn = MongoDBConnection(self.db_name)
        self.db = self.mongo_conn.get_db(self.db_name)

    def create(self, collection_name, schema=None):
        try:
            # Check if the collection already exists
            if collection_name in self.db.list_collection_names():
                return {"message": f"Collection '{collection_name}' already exists"}

            # Create the collection
            self.db.create_collection(collection_name)

            # Add validation rules using the insert command
            if schema:
                self.db.command({
                    "collMod": collection_name,
                    "validator": {"$jsonSchema": schema}
                })

            return {"message": f"Collection '{collection_name}' created successfully"}
        except Exception as e:
            print(f"Error creating collection: {str(e)}")
            return {"error": f"Error creating collection: {str(e)}"}
        

    def update(self, collection_name, new_collection_name):
        try:
            # Check if the original collection exists
            if collection_name not in self.db.list_collection_names():
                return {"error": f"Collection '{collection_name}' does not exist"}

            # Check if the new collection name already exists
            if new_collection_name in self.db.list_collection_names():
                return {"error": f"Collection '{new_collection_name}' already exists"}

            # Rename the original collection to the new name
            self.db[collection_name].rename(new_collection_name)
            return {"message": f"Collection '{collection_name}' renamed to '{new_collection_name}' successfully"}
        except Exception as e:
            # Handle any exceptions here
            print(f"Error updating collection: {str(e)}")
            return {"error": f"Error updating collection: {str(e)}"}
        
    def delete(self, collection_name):
        try:
            # Check if the collection exists before attempting to delete
            if collection_name not in self.db.list_collection_names():
                return {"error": f"Collection '{collection_name}' does not exist"}

            # Delete the collection
            self.db.drop_collection(collection_name)
            return {"message": f"Collection '{collection_name}' deleted successfully"}
        except Exception as e:
            # Handle any exceptions here
            print(f"Error deleting collection: {str(e)}")
            return {"error": f"Error deleting collection: {str(e)}"}

    def close_connection(self):
        self.mongo_conn.close()


class MongoDBCollections:
    def __init__(self, db_name=None):
        self.db_name = db_name or settings.DATABASES['default']['NAME']  # Use the default database name
        self.mongo_conn = MongoDBConnection(self.db_name)
        self.db = self.mongo_conn.get_db(self.db_name)

    # Create a document in the collection
    def create_document(self, collection_name, data):
        try:
            collection = self.db[collection_name]
            result = collection.insert_one(data)
            return result.inserted_id
        except Exception as e:
            # Log the error
            print(f"Error creating document in collection '{collection_name}': {str(e)}")
            # Re-raise the exception to handle it at a higher level if needed
            raise
    # Read documents from the collection based on a query
    def read_documents(self, collection_name, query={}):
        try:
            collection = self.db[collection_name]
            documents = collection.find(query)
            return list(documents)
        except Exception as e:
            # Handle any exceptions here
            print(f"Error reading documents: {str(e)}")

    # Update a document in the collection based on a query
    def update_document(self, collection_name, query, data):
        try:
            collection = self.db[collection_name]
            result = collection.update_one(query, {"$set": data})
            return result.modified_count
        except Exception as e:
            # Handle any exceptions here
            print(f"Error updating document: {str(e)}")

    # Delete a document from the collection based on a query
    def delete_document(self, collection_name, query):
        try:
            collection = self.db[collection_name]
            result = collection.delete_one(query)
            return result.deleted_count
        except Exception as e:
            # Handle any exceptions here
            print(f"Error deleting document: {str(e)}")

    def close_connection(self):
        self.mongo_conn.close()


