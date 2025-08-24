# animal_shelter.py

# Author: Zach Fizet
# Customized for CS-340 Project Two
# MongoDB CRUD operations wrapper for Dash dashboard

from pymongo import MongoClient, errors

class AnimalShelter:
    def __init__(self, username, password, host="localhost", port=27017, db_name="AAC", collection_name="animals"):
        """
        Initialize the MongoDB connection using provided credentials.
        """
        try:
            uri = f"mongodb://{username}:{password}@{host}:{port}/?authSource=admin"
            self.client = MongoClient(uri)
            self.client.admin.command("ping")
            print("MongoDB connection successful.")
        except errors.ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
            self.client = None

        # Set default database and collection
        self.db_name = db_name
        self.collection_name = collection_name
        self.database = self.client[self.db_name]
        self.collection = self.database[self.collection_name]

    # ---------------- CREATE ----------------
    def create(self, document):
        """
        Insert a single document.
        :param document: dict containing the record to insert
        :return: True if insert successful, False otherwise
        """
        if self.client is None:
            print("No MongoDB client.")
            return False
        try:
            result = self.collection.insert_one(document)
            return result.acknowledged
        except Exception as e:
            print(f"Insert failed: {e}")
            return False

    # NEW: Create multiple documents at once
    def create_many(self, documents):
        """
        Insert multiple documents into the collection.
        :param documents: list of dicts containing the records to insert
        :return: number of successfully inserted documents
        """
        if self.client is None:
            print("No MongoDB client.")
            return 0
        try:
            result = self.collection.insert_many(documents)
            return len(result.inserted_ids)
        except Exception as e:
            print(f"Bulk insert failed: {e}")
            return 0

    # ---------------- READ ----------------
    def read(self, query):
        """
        Read documents from collection based on query.
        :param query: dict for MongoDB query
        :return: List of matching documents
        """
        if self.client is None:
            print("No MongoDB client.")
            return []
        try:
            return list(self.collection.find(query))
        except Exception as e:
            print(f"Read failed: {e}")
            return []

    # ---------------- UPDATE ----------------
    def update(self, query, new_values):
        """
        Update multiple documents matching query with new values.
        :param query: dict specifying which documents to update
        :param new_values: dict with fields to update
        :return: count of modified documents
        """
        if self.client is None:
            return 0
        try:
            result = self.collection.update_many(query, {"$set": new_values})
            return result.modified_count
        except Exception as e:
            print(f"Update failed: {e}")
            return 0

    # NEW: Update a single document
    def update_one(self, query, new_values):
        """
        Update a single document matching query with new values.
        Useful for 'edit' functionality in dashboards.
        :param query: dict specifying which document to update
        :param new_values: dict with fields to update
        :return: True if document was updated, False otherwise
        """
        if self.client is None:
            return False
        try:
            result = self.collection.update_one(query, {"$set": new_values})
            return result.modified_count > 0
        except Exception as e:
            print(f"Single update failed: {e}")
            return False

    # ---------------- DELETE ----------------
    def delete(self, query):
        """
        Delete multiple documents matching query.
        :param query: dict specifying which documents to delete
        :return: count of deleted documents
        """
        if self.client is None:
            return 0
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except Exception as e:
            print(f"Delete failed: {e}")
            return 0

    # NEW: Delete a single document
    def delete_one(self, query):
        """
        Delete a single document matching query.
        Useful for dashboard row-delete functionality.
        :param query: dict specifying which document to delete
        :return: True if document was deleted, False otherwise
        """
        if self.client is None:
            return False
        try:
            result = self.collection.delete_one(query)
            return result.deleted_count > 0
        except Exception as e:
            print(f"Single delete failed: {e}")
            return False
