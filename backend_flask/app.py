from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
import time
from bson.objectid import ObjectId
import datetime

# initial flask cors and pymongo
app = Flask(__name__)
cors = CORS(app)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/D4C"
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
    db_check = user_collection.find({"name": username_register}).count() > 0
    print(db_check)
    if not db_check:
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
    username_login = post_data.get('username_login')
    password_login = post_data.get('password_login')
    user_info_to_check = {
        'name': username_login,
        'password': password_login
    }
    db_check = user_collection.find_one(user_info_to_check)
    if db_check is not None:
        return jsonify({
            'success': True,
            'message': 'successfully logged in',
            'current_username': username_login
        })
    else:
        return jsonify({
            'success': False,
            'message': 'wrong password or user not exist'
        })

# add post
@app.route("/add_post", methods=['POST', 'GET'])
def add_post():
    post_data = request.get_json()
    add_post_title = post_data.get('add_post_title')
    picked_tag = post_data.get('picked_tag')
    add_post_content = post_data.get('add_post_content')
    creator = post_data.get('creator')
    post_info_to_insert = {
        'post_title': add_post_title,
        'post_tag': picked_tag,
        'post_content': add_post_content,
        'creator': creator
    }
    db_insert = post_collection.insert_one(post_info_to_insert)
    return jsonify({
        'success': True,
        'message': 'post successfully added'
    })


# display all post
@app.route("/display_all_post", methods=['POST', 'GET'])
def display_all_post():
    post_data = request.get_json()
    # add_post_title = post_data.get('add_post_title')
    # picked_tag = post_data.get('picked_tag')
    # add_post_content = post_data.get('add_post_content')
    # post_info_to_insert = {
    #     'post_title': add_post_title,
    #     'tag': picked_tag,
    #     'post_content': add_post_content
    # }
    all_document_cursor = post_collection.find({})
    all_posts = []

    for every_post in all_document_cursor:
        every_post_info = every_post
        # reference: https://blog.csdn.net/u011744758/article/details/50085013
        # https://blog.csdn.net/GeekLeee/article/details/77767969
        local_time = every_post_info["_id"].generation_time - datetime.timedelta(hours=6)
        every_post_info["time"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
        every_post_info["_id"] = str(every_post_info["_id"])
        all_posts.append(every_post_info)

    return jsonify({
        'success': True,
        'message': 'All post successfully displayed',
        "all_posts": all_posts
    })

@app.route("/delete_post", methods=['POST', 'GET'])
def delete_post():
    post_data = request.get_json()
    post_collection.remove({"_id": ObjectId(post_data['delete_id'])})
    return jsonify({
        'success': True,
        'message': 'Delete post successfully',
    })

@app.route("/edit_post", methods=['POST', 'GET'])
def edit_post():
    post_data = request.get_json()
    id = post_data["edit_id"]
    new_title = post_data["edit_form"]["edit_title"]
    new_content = post_data["edit_form"]["edit_content"]
    creator = post_data["edit_form"]["creator"]
    post_collection.update({"_id": ObjectId(id)}, {
        'post_title': new_title,
        'post_content': new_content,
        'creator': creator,
    })
    return jsonify({
        'success': True,
        'message': 'Edit post successfully',
    })

##88009
# @app.route('/')
# def hello_world():
#     dbfindresult = mongo.db.testdb.find()
#     for r in dbfindresult:
#         print(r['name'])
#     return "Hello world!"

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
