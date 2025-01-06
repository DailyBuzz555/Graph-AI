# Phase 1: Knowledge Graph Schema and API Setup

# Step 1: Neo4j Schema Setup
from neo4j import GraphDatabase

def create_graph_schema(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def create_constraints(tx):
        tx.run("CREATE CONSTRAINT ON (t:Topic) ASSERT t.id IS UNIQUE")
        tx.run("CREATE CONSTRAINT ON (r:Resource) ASSERT r.id IS UNIQUE")
        tx.run("CREATE CONSTRAINT ON (u:User) ASSERT u.id IS UNIQUE")

    with driver.session() as session:
        session.write_transaction(create_constraints)
        print("Constraints created successfully!")

    driver.close()

# Example Usage
# create_graph_schema("bolt://localhost:7687", "neo4j", "password")

# Step 2: Create API Endpoints using FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Mock database connection (replace with Neo4j queries)
mock_db = {
    "topics": [
        {"id": 1, "name": "Introduction to Python", "prerequisites": [], "difficulty": "Easy"},
        {"id": 2, "name": "Data Structures in Python", "prerequisites": [1], "difficulty": "Medium"},
        {"id": 3, "name": "Machine Learning Basics", "prerequisites": [2], "difficulty": "Hard"},
    ],
    "users": [
        {"id": 1, "name": "Alice", "progress": [1]},
    ]
}

class ProgressUpdate(BaseModel):
    user_id: int
    topic_id: int

@app.get("/topics")
def get_topics():
    return mock_db["topics"]

@app.get("/users/{user_id}/progress")
def get_user_progress(user_id: int):
    user = next((u for u in mock_db["users"] if u["id"] == user_id), None)
    if user:
        return {"progress": user["progress"]}
    return {"error": "User not found"}

@app.post("/users/progress")
def update_progress(progress: ProgressUpdate):
    user = next((u for u in mock_db["users"] if u["id"] == progress.user_id), None)
    if user:
        if progress.topic_id not in user["progress"]:
            user["progress"].append(progress.topic_id)
        return {"message": "Progress updated", "progress": user["progress"]}
    return {"error": "User not found"}

@app.get("/users/{user_id}/recommendations")
def get_recommendations(user_id: int):
    user = next((u for u in mock_db["users"] if u["id"] == user_id), None)
    if user:
        completed = set(user["progress"])
        recommendations = [
            topic for topic in mock_db["topics"]
            if set(topic["prerequisites"]).issubset(completed) and topic["id"] not in completed
        ]
        return {"recommendations": recommendations}
    return {"error": "User not found"}

# To run this app:
# 1. Save the file as app.py
# 2. Run `uvicorn app:app --reload` in the terminal
# 3. Access the endpoints at http://127.0.0.1:8000
