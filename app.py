import os
from os.path import join, dirname
from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    list_receive = request.form['bucket_list']
    print(list_receive)
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num':num,
        'bucket': list_receive,
        'done':0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Wish Saved'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        {'num': int(num_receive)},
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Congratulations'})

@app.route("/delete", methods=["POST"])
def bucket_delete():
    num_receive_delete = request.form['num_give_delete']
    db.bucket.delete_one(
        {'num': int(num_receive_delete)}
    )
    return jsonify({'msg': 'Deleted'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_items = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets': bucket_items})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)