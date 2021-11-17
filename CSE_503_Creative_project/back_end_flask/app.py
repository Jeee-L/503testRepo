# all import
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
# initial flask cors and pymongo
app = Flask(__name__)
cors = CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/D4C"
mongo = PyMongo(app)

# get all collections
# refer to https://www.w3schools.com/python/python_mongodb_insert.asp
user_collection = mongo.db.USER
post_collection = mongo.db.ALL_POST
# register
@app.route("/register", methods=['POST', 'GET'])
def register():
    post_data = request.get_json()
    username_register = post_data.get('username_register')
    password_register = post_data.get('password_register')
    user_info_to_insert = {
        'name': username_register,
        'password': password_register
    }
    # check user existed or not
    # https://docs.mongodb.com/manual/reference/method/db.collection.findOne/
    db_check = user_collection.find_one({}, {username_register: 1})
    print(db_check)
    if db_check is None:
        db_insert = user_collection.insert_one(user_info_to_insert)
        return jsonify({
            'success': True,
            'message': 'successfully registered'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'user exist'
        })


# log in
@app.route("/login", methods=['POST', 'GET'])
def login():
    post_data = request.get_json()
    username_register = post_data.get('username_login')
    password_register = post_data.get('password_login')
    user_info_to_check = {
        'name': username_register,
        'password': password_register
    }
    db_check = user_collection.find_one(user_info_to_check)
    if db_check is not None:
        return jsonify({
            'success': True,
            'message': 'successfully logged in '
        })
    else:
        return jsonify({
            'success': False,
            'message': 'wrong password or user not exist'
        })


##88009
# @app.route('/')
# def hello_world():
#     dbfindresult = mongo.db.testdb.find()
#     for r in dbfindresult:
#         print(r['name'])
#     return "Hello world!"
#
# # @app.route("/test", methods=['GET'])
# # def test():
# #     post_data = request.get_json()
# #     dbfindresult = mongo.db.testdb.find()
# #     for r in dbfindresult:
# #         result = r['name']
# #     print(result)
# #     return (result)

if __name__ == '__main__':
    app.run()
