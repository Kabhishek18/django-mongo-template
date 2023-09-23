from django.shortcuts import render
import json
from django.http import JsonResponse
from herkey.services.mongo import MongoDBConnection,MongoDBUtility, MongoDBCollections  
from bson import ObjectId
from datetime import datetime

def create_collections(request):
    try:
        json_file_path = 'migrations/migrate_copy.json'
        mongo_utility = MongoDBUtility()

        with open(json_file_path, 'r') as file:
            data = json.load(file)
        created_collections = {} 
        for collection_data in data:
            collection_name = collection_data['collection_name']
            schema = collection_data['schema']
            created_collections[collection_name] = mongo_utility.create(collection_name, schema)
        return JsonResponse(created_collections)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def insert_sample_data(sample_data, collection_name):
    try:
        mongo_utility = MongoDBUtility()
        mongo_collections = MongoDBCollections()
        for data in sample_data:
            mongo_collections.create_document(collection_name, data)
        mongo_utility.close_connection()
        mongo_collections.close_connection()

        return {"message": f"Sample {collection_name} insertion completed successfully"}
    except Exception as e:
        error_message = f"Error inserting sample data: {str(e)}"
        return {"error": error_message}


def sample_data_uploader(reqest):
    try:
        sample_data_user = [
            {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "password123",
                "firstName": "John",
                "lastName": "Doe",
                "dob": "asdasd",
                "roles": "user",
                "active": ["active"],
                "createdBy": ObjectId("65098459e61cf8776b7601aa"), 
                "createdAt": datetime.utcnow(),  
                "updatedAt": datetime.utcnow(),  
            },
            {
            "username": "jane_smith",
            "email": "jane@example.com",
            "password": "pass456",
            "firstName": "Jane",
            "lastName": "Smith",
            "dob": datetime.strptime("1990-01-15", "%Y-%m-%d"),
            "roles": "user",
            "active": ["active"],
            "createdBy": ObjectId("65098459e61cf8776b7601ab"),
            "createdAt": datetime.utcnow(),  
            "updatedAt": datetime.utcnow(),  
            },
        ]

        sample_data_groups_category = [
           {
                "name": "Category 1",
                "createdBy": ObjectId("650985b0d4d987470f2a98e6"),  # Correct ObjectId here
                "createdAt": datetime.utcnow(),  # Provide the current datetime
                "updatedAt": datetime.utcnow(),  # Provide the current datetime
            },
            {
                "name": "Category 2",
                "createdBy": ObjectId("650985b0d4d987470f2a98e7"),  # Correct ObjectId here
                "createdAt": datetime.utcnow(),  # Provide the current datetime
                "updatedAt": datetime.utcnow(),  # Provide the current datetime
            },
        ]

        sample_data_groups_collection = [
            {
                "group_name": "Group A",
                "public_or_private": "public",  # Specify if the group is public or private
                "about": "This is Group A",
                "created_by": {
                    "admin_moderator_id": ObjectId("65098a208f585af1ff079467")  # Correct ObjectId here
                },
                "group_rules": "No spamming allowed",
                "description": "A public group",
                "group_category": ObjectId("650985b0d4d987470f2a98e6"),  # Correct ObjectId here
                "company": [],  # List of associated company IDs (if applicable)
                "featured": True,
                "banner_url": "https://example.com/banner1.jpg",
                "icon_url": "https://example.com/icon1.jpg",
                "created_at": datetime.utcnow(),  # Current datetime
                "edited_at": datetime.utcnow(),  # Current datetime
            },
            {
                "group_name": "Group B",
                "public_or_private": "private",  # Specify if the group is public or private
                "about": "This is Group B",
                "created_by": {
                    "admin_moderator_id": ObjectId("65098a208f585af1ff079468")  # Correct ObjectId here
                },
                "group_rules": "Be respectful to others",
                "description": "A private group",
                "group_category": ObjectId("650985b0d4d987470f2a98e7"),  # Correct ObjectId here
                "company": [],  # List of associated company IDs (if applicable)
                "featured": False,
                "banner_url": "https://example.com/banner2.jpg",
                "icon_url": "https://example.com/icon2.jpg",
                "created_at": datetime.utcnow(),  # Current datetime
                "edited_at": datetime.utcnow(),  # Current datetime
            },
        ]

        sample_data_groups_join_requests = [
            {
                "user_id": ObjectId("65098459e61cf8776b7601aa"),  # Correct ObjectId here
                "group_id": ObjectId("65098a208f585af1ff079467"),  # Correct ObjectId here
                "role": "member",
                "request_date": datetime(2023, 9, 19),  # Provide a datetime object
                "status": "pending",
                "reason": "Interested in joining",
                "approval": {
                    "$date": datetime.utcnow(),  # Provide a datetime object
                    "approved_by": ObjectId("65098459e61cf8776b7601ab"),  # Correct ObjectId here
                },
                "updated": {
                    "$date": datetime.utcnow(),  # Provide a datetime object
                    "updated_by": ObjectId("65098459e61cf8776b7601ab"),  # Correct ObjectId here
                },
            },
            {
                "user_id": ObjectId("65098459e61cf8776b7601ab"),  # Correct ObjectId here
                "group_id": ObjectId("65098a208f585af1ff079468"),  # Correct ObjectId here
                "role": "member",
                "request_date": datetime(2023, 9, 18),  # Provide a datetime object
                "status": "approved",
                "reason": "Excited to join",
                "approval": {
                    "$date": datetime.utcnow(),  # Provide a datetime object
                    "approved_by": ObjectId("65098459e61cf8776b7601ac"),  # Correct ObjectId here
                },
                "updated": {
                    "$date": datetime.utcnow(),  # Provide a datetime object
                    "updated_by": ObjectId("65098459e61cf8776b7601ac"),  # Correct ObjectId here
                },
            },
        ]


 
        sample_data_group_users = [
            {
                "user_id": ObjectId("65098459e61cf8776b7601aa"),  # Correct ObjectId here
                "group_id": ObjectId("65098a208f585af1ff079467"),  # Correct ObjectId here
                "status": "active",
                "joined_at": datetime(2023, 9, 19),  # Provide a datetime object
                "role": "member",
            },
            {
                "user_id": ObjectId("65098459e61cf8776b7601ab"),  # Correct ObjectId here
                "group_id": ObjectId("65098a208f585af1ff079468"),  # Correct ObjectId here
                "status": "active",
                "joined_at": datetime(2023, 9, 18),  # Provide a datetime object
                "role": "member",
            },
        ]
        data = {}
        data['user'] = insert_sample_data(sample_data_user,"user")
        data['groups_category'] =insert_sample_data(sample_data_groups_category,"groups_category")
        data['groups_collection']= insert_sample_data(sample_data_groups_collection,"groups_collection")
        data['groups_join_requests'] = insert_sample_data(sample_data_groups_join_requests,"groups_join_requests")
        data['group_users'] = insert_sample_data(sample_data_group_users,"group_users")

        return JsonResponse({"message": "Sample data insertion completed successfully", "data": data})
 
    except Exception as e:
        error_message = f"Error inserting sample data: {str(e)}"
        return JsonResponse({"error": error_message}, status=500)
    

def delete_collection(collection_name):
    try:
        mongo_utility = MongoDBUtility()
        result = mongo_utility.delete(collection_name)
        mongo_utility.close_connection()

        if "error" in result:
            return JsonResponse({"error": result["error"]}, status=400)
        else:
            return JsonResponse({"message": result["message"]})

    except Exception as e:
        error_message = f"Error deleting collection: {str(e)}"
        return JsonResponse({"error": error_message}, status=500)

    
def delete_all(request):
    try:
        data = {}
        data['user'] = delete_collection("user")
        data['groups_category'] = delete_collection("groups_category")
        data['groups_collection'] = delete_collection("groups_collection")
        data['groups_join_requests'] = delete_collection("groups_join_requests")
        data['group_users'] = delete_collection("group_users")

        # Check if any of the delete operations resulted in an error
        for key, response in data.items():
            if "error" in response:
                return JsonResponse({"error": response["error"]}, status=500)

        # If all deletions were successful, return a success message
        return JsonResponse({"message": "All collections deleted successfully"})

    except Exception as e:
        error_message = f"Error deleting collections: {str(e)}"
        return JsonResponse({"error": error_message}, status=500)
