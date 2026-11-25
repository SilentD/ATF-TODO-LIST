import os 
import streamlit as st
from pymongo import MongoClient 
class DatabaseConfig: 
    _instance = None
    _client = None 
    @classmethod 
    def get_client(cls) -> MongoClient: 
        if cls._client is None: 
      # Check Streamlit Cloud Secrets first, fallback to OS environment variable 
            mongo_uri = st.secrets.get("MONGO_URI", os.getenv("MONGO_URI", "mongodb://localhost:27017")) 
            cls._client = MongoClient(mongo_uri)
        return cls._client 
    @classmethod
    def get_database(cls, db_name:str = "atf_todo_db"):
        return cls.get_client()[db_name]
  
db_config = DatabaseConfig()
