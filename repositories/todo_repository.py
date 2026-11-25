from bson import ObjectId
from datetime import datetime, timezone 
from utils.db_config import db_config
class TodoRepository: 
    def __init__(self): 
        self.collection = db_config.get_database()["tasks"]
    def create_task(self, title: str, category: str, assignee: str) -> str:
          doc = { "title": title,
                "category": category,
                "assignee": assignee, 
                "completed": False,
                "created_at": datetime.now(timezone.utc) 
                }
          result = self.collection.insert_one(doc)
          return str(result.inserted_id)
    def get_all_tasks(self) -> list[dict]:
        tasks = list(self.collection.find().sort("created_at", -1)) 
        for task in tasks:
            task["_id"] = str(task["_id"]) 
        return tasks
    def toggle_task(self, task_id: str, current_status: bool): 
        self.collection.update_one( {"_id": ObjectId(task_id)},
                                    {"$set": {"completed": not current_status}} )
    def delete_task(self, task_id: str): 
        self.collection.delete_one({"_id": ObjectId(task_id)})