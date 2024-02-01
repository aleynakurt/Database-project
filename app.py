from flask import Flask,jsonify, Response, request
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import json
import os


app = Flask(__name__)

mongo_db_host = os.environ.get('MONGO_DB_HOST', 'localhost')
mongo_db_port = int(os.environ.get('MONGO_DB_PORT', 27017))
mongo_db_name = os.environ.get('MONGO_DB_NAME', 'books')
mongo_db_collection = os.environ.get('MONGO_DB_COLLECTION', 'bookstore')

print("mongo_db_host: ", mongo_db_host)
print("mongo_db_port: ", mongo_db_port)
print("mongo_db_name: ", mongo_db_name)
print("mongo_db_collection: ", mongo_db_collection)



client = MongoClient('mongodb://localhost:27017/')
db = client['books']
collection = db['bookstore']

@app.route('/world/api/v1.0/bookstore', methods=['GET'])
def books():
    books_list = list(collection.find({}, {'_id': False}))
    response = Response(response=json.dumps({"books": books_list}, indent=2), status=200, mimetype="application/json")
    return response


@app.route('/world/api/v1.0/bookstore/<string:book_id>', methods=['GET'])
def fetch_book(book_id):
    book = collection.find_one({"_id": ObjectId(book_id)}, {'_id': 'ObjectId'})
    return jsonify(book)

@app.route('/world/api/v1.0/bookstore', methods=['POST'])
def add_book():
    new_book = request.json
    result = collection.insert_one(new_book)
    return jsonify({"inserted_id": str(result.inserted_id)})

@app.route('/world/api/v1.0/bookstore/<string:book_id>', methods=['PUT'])
def update_book(book_id):
    updated_book = request.json
    result = collection.update_one({"_id": ObjectId(book_id)}, {"$set": updated_book})
    return jsonify({"modified_count": result.modified_count})

@app.route('/world/api/v1.0/bookstore/<string:book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = collection.delete_one({"_id": ObjectId(book_id)})
    return jsonify({"deleted_count": result.deleted_count})


if __name__ == '__main__':
    app.run(port=50505, debug=True)



#http://127.0.0.1:50505/world/api/v1.0/bookstore






