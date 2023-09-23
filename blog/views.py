from django.shortcuts import render
from django.http import JsonResponse
from herkey.services.mongo import MongoDBUtility, MongoDBCollections  

def create_user_collection(request):
    try:
        # Replace 'herkey' with your actual database name
        db_name = 'herkey'
        mongo_utility = MongoDBUtility(db_name)
        collection_name = 'rabish'
        user_schema = {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'minLength': 3},
                    'email': {'type': 'string'},
                    'age': {'type': 'number', 'minimum': 18},
                },
                'required': ['username', 'email'],
            }

        mongo_utility.create(collection_name, schema=user_schema)
        mongo_utility.close_connection()
        return JsonResponse({"message": collection_name + " collection created successfully"})
    except Exception as e:
        print(f"Error creating "+collection_name+" collection: {str(e)}")
        return JsonResponse({"error": f"Error creating "+collection_name+" collection: {str(e)}"}, status=500)


def add_user(request):
    try:
        # Extract user_data from the request (assuming it's sent as JSON)
        user_data = {
            "username": "rahul",
            "email": "rahul@example.com",
            "age": 22
        }  # Adjust this based on how you receive data

        # Replace 'herkey' with your actual database name
        db_name = 'herkey'
        collection_name = 'users'

        mongo_utility = MongoDBCollections(db_name)
        result = mongo_utility.create_document(collection_name, user_data)
        mongo_utility.close_connection()

        if result:
            return JsonResponse({"message": f"User added with ID: {result}"})
        else:
            return JsonResponse({"error": "Error adding user."}, status=500)
    except Exception as e:
        return JsonResponse({"error": f"Error adding user: {str(e)}"}, status=500)