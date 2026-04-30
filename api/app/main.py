import os
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import mysql.connector

app = FastAPI()

MONGO_URI = os.getenv("MONGO_URI")

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER_API")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD_API")


def get_mongo_posts():
    client = MongoClient(MONGO_URI)
    db = client.get_database()
    posts = list(db.posts.find({}, {"_id": 0}))
    client.close()
    return posts


def get_mysql_users():
    conn = mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        database=MYSQL_DB,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nom, email FROM utilisateurs")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


@app.get("/")
def root():
    return {"message": "API hybride MongoDB + MySQL"}


@app.get("/posts")
def posts():
    try:
        return get_mongo_posts()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MongoDB error: {str(e)}")


@app.get("/users")
def users():
    try:
        return get_mysql_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"MySQL error: {str(e)}")


@app.get("/test")
def health():
    try:
        posts_data = get_mongo_posts()
        users_data = get_mysql_users()
        return {
            "status": "ok",
            "mongo_posts_count": len(posts_data),
            "mysql_users_count": len(users_data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))