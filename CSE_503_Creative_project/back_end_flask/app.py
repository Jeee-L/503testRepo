from flask import Flask, request
from flask_cors import CORS
from flask_pymongo import PyMongo

app = Flask(__name__)
cors = CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
mongo = PyMongo(app)
88009
@app.route('/')
def hello_world():
    dbfindresult = mongo.db.testdb.find()
    for r in dbfindresult:
        print(r['name'])
    return "Hello world!"

@app.route("/test", methods=['GET'])
def test():
    post_data = request.get_json()
    dbfindresult = mongo.db.testdb.find()
    for r in dbfindresult:
        result = r['name']
    print(result)
    return (result)


if __name__ == '__main__':
    app.run()