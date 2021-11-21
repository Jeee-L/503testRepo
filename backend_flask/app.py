import bson
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
        'password': password_register,
        'friend_list': [],
        'notification_list': [],
        'post_shared_to_you_list': [],
        'post_you_share_to_other_list': []
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
        'creator': creator,
        'all_comments': [],
        'all_likes': []
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
    # get current user friend list to share post
    current_user = post_data["current_user"]
    # print(current_user)
    current_user_info = user_collection.find_one({"name": current_user})
    current_user_friend_list = []
    if current_user_info is not None:
        current_user_friend_list = current_user_info['friend_list']
    # print(current_user_friend_list)
    # get all post
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
        "all_posts": all_posts,
        "friend_list": current_user_friend_list
    })


@app.route("/delete_post", methods=['POST', 'GET'])
def delete_post():
    post_data = request.get_json()
    post_collection.remove({"_id": ObjectId(post_data['delete_id'])})
    return jsonify({
        'success': True,
        'message': 'Delete post successfully'
    })


@app.route("/edit_post", methods=['POST', 'GET'])
def edit_post():
    post_data = request.get_json()
    id = post_data["edit_id"]
    new_title = post_data["edit_form"]["edit_title"]
    new_content = post_data["edit_form"]["edit_content"]
    new_tag = post_data["edit_form"]["edit_tag"]
    creator = post_data["edit_form"]["creator"]
    post_collection.update({"_id": ObjectId(id)}, {
        'post_title': new_title,
        'post_content': new_content,
        'post_tag': new_tag,
        'creator': creator,
    })
    return jsonify({
        'success': True,
        'message': 'Edit post successfully'
    })


@app.route("/send_friend_request", methods=['POST', 'GET'])
def send_friend_request():
    post_data = request.get_json()
    username_to_send_friend_request = post_data["username_to_send_friend_request"]
    username_to_receive_friend_request = post_data["username_to_receive_friend_request"]
    # print(post_data)
    user_collection.update({"name": username_to_receive_friend_request}, {'$push':
        {
            'notification_list': username_to_send_friend_request}
    })
    return jsonify({
        'success': True,
        'message': 'send friend request successfully'
    })


@app.route("/notification", methods=['POST', 'GET'])
def notification():
    post_data = request.get_json()
    username_to_receive_notification = post_data["current_user"]
    # print(post_data)
    current_user_info = user_collection.find_one({"name": username_to_receive_notification})
    notification_list = current_user_info["notification_list"]

    return jsonify({
        'success': True,
        'message': 'send friend request successfully',
        "notification_list": notification_list
    })


@app.route("/refuse", methods=['POST', 'GET'])
def refuse():
    post_data = request.get_json()
    refuse_username = post_data["refuse_username"]
    current_user = post_data["current_user"]
    current_user_info = user_collection.update({"name": current_user},
                                               {'$pull':
                                                    {"notification_list": refuse_username}
                                                })
    return jsonify({
        'success': True,
        'message': 'Refused friend request successfully'
    })


@app.route("/accept", methods=['POST', 'GET'])
def accept():
    post_data = request.get_json()
    accept_username = post_data["accept_username"]
    current_user = post_data["current_user"]
    user_collection.update({"name": current_user},
                           {'$pull':
                                {"notification_list": accept_username}
                            })
    user_collection.update({"name": current_user}, {'$push':
                                                        {'friend_list': accept_username}
                                                    })
    user_collection.update({"name": accept_username}, {'$push':
                                                           {'friend_list': current_user}
                                                       })
    return jsonify({
        'success': True,
        'message': 'accept friend request successfully'
    })


@app.route("/display_friend_list", methods=['POST', 'GET'])
def display_friend_list():
    post_data = request.get_json()
    current_user = post_data["current_user"]

    user_info = user_collection.find_one(({"name": current_user}))
    friend_list = user_info["friend_list"]
    return jsonify({
        'success': True,
        'message': 'Display friend list successfully',
        'friend_list': friend_list
    })


@app.route("/unfriend", methods=['POST', 'GET'])
def unfriend():
    post_data = request.get_json()
    username_to_unfriend = post_data["username_to_unfriend"]
    current_user = post_data["current_user"]
    user_collection.update({"name": current_user},
                           {'$pull':
                                {"friend_list": username_to_unfriend}
                            })
    user_collection.update({"name": username_to_unfriend},
                           {'$pull':
                                {'friend_list': current_user}
                            })
    return jsonify({
        'success': True,
        'message': 'Unfriend successfully'
    })


@app.route("/share_post", methods=['POST', 'GET'])
def share_post():
    post_data = request.get_json()
    shared_to_username = post_data["shared_to_username"]
    shared_from_username = post_data["shared_from_username"]
    shared_post_id = post_data["shared_post_id"]
    user_collection.update({"name": shared_to_username}, {'$push':
        {"post_shared_to_you_list":
             {"shared_post_id" : shared_post_id,
             "shared_from_username" : shared_from_username}}
    })
    user_collection.update({"name": shared_from_username}, {'$push':
        {"post_you_share_to_other_list":
            {"shared_post_id" : shared_post_id,
             "shared_to_username" : shared_to_username}}
    })
    return jsonify({
        'success': True,
        'message': 'Post shared successfully'
    })


@app.route("/display_all_share_post_to_others", methods=['POST', 'GET'])
def display_all_share_post_to_others():
    post_data = request.get_json()
    # get current user friend list to share post
    current_user = post_data["current_user"]
    current_user_info = user_collection.find_one({"name": current_user})
    all_share_post_to_others_list = {}
    # print(current_user_info)
    # print(current_user_info['post_you_share_to_other_list'])
    if (current_user_info is not None) and (current_user_info['post_you_share_to_other_list']):
        # print(11111)
        all_share_post_to_others = current_user_info['post_you_share_to_other_list']
        # print(all_share_post_to_others)
        # refer to https://docs.mongodb.com/manual/reference/operator/query/in/
        # refer to https://stackoverflow.com/questions/46752051/flask-pymongo-string-back-to-objectid
        for every_shared_post in all_share_post_to_others:
            # print(every_shared_post)
            every_share_post_id = ObjectId(every_shared_post["shared_post_id"])
            every_shared_post_info = post_collection.find_one({'_id': every_share_post_id})
            if every_shared_post_info is not None:
                every_post_info_returned = every_shared_post_info
                # reference: https://blog.csdn.net/u011744758/article/details/50085013
                # https://blog.csdn.net/GeekLeee/article/details/77767969
                local_time = every_shared_post_info["_id"].generation_time - datetime.timedelta(hours=6)
                every_post_info_returned["time"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
                every_post_info_returned["_id"] = str(every_shared_post_info["_id"])
                every_post_info_returned["username_this_post_shared_to"] = every_shared_post['shared_to_username']
                all_share_post_to_others_list[every_shared_post_info["_id"]] = every_post_info_returned

        return jsonify({
            'success': True,
            'message': 'All shared post successfully displayed',
            "all_share_post_to_others_list": all_share_post_to_others_list
        })
    else:
        return jsonify({
            'success': True,
            'message': 'log in to see your post shared to others',
            "all_share_post_to_others_list": all_share_post_to_others_list
        })


@app.route("/withdraw_shared_post", methods=['POST', 'GET'])
def withdraw_shared_post():
    post_data = request.get_json()
    print(post_data)
    username_this_post_shared_to = post_data["username_this_post_shared_to"]
    current_user = post_data["current_user"]
    withdraw_shared_post_id = post_data["withdraw_shared_post_id"]
    # https://docs.mongodb.com/manual/reference/operator/update/unset/
    user_collection.update(
        {"name": current_user},
        {"$pull":
             {"post_you_share_to_other_list":
                  {"shared_post_id" : withdraw_shared_post_id,
                    "shared_to_username" : username_this_post_shared_to
                   }
              }
        }
    )
    user_collection.update(
        {"name": username_this_post_shared_to},
        {"$pull":
             {"post_shared_to_you_list":
                  {"shared_post_id": withdraw_shared_post_id,
                   "shared_from_username": current_user
                   }
              }
         }
    )
    return jsonify({
        'success': True,
        'message': 'Withdraw shared post successfully'
    })


@app.route("/display_all_share_post_to_you", methods=['POST', 'GET'])
def display_all_share_post_to_you():
    post_data = request.get_json()
    # get current user friend list to share post
    current_user = post_data["current_user"]
    current_user_info = user_collection.find_one({"name": current_user})
    post_shared_to_you_list = {}
    # print(current_user_info)
    if (current_user_info is not None) and (current_user_info['post_shared_to_you_list']):
        # print(11111)
        all_share_post_to_you = current_user_info['post_shared_to_you_list']
        # print(all_share_post_to_others)
        # refer to https://docs.mongodb.com/manual/reference/operator/query/in/
        # refer to https://stackoverflow.com/questions/46752051/flask-pymongo-string-back-to-objectid
        for every_shared_post in all_share_post_to_you:
            every_share_post_id = ObjectId(every_shared_post["shared_post_id"])
            every_shared_post_info = post_collection.find_one({'_id': every_share_post_id})
            print(every_shared_post_info)
            if every_shared_post_info is not None:
                every_post_info_returned = every_shared_post_info
                # reference: https://blog.csdn.net/u011744758/article/details/50085013
                # https://blog.csdn.net/GeekLeee/article/details/77767969
                local_time = every_shared_post_info["_id"].generation_time - datetime.timedelta(hours=6)
                every_post_info_returned["time"] = local_time.strftime("%Y-%m-%d %H:%M:%S")
                every_post_info_returned["_id"] = str(every_shared_post_info["_id"])
                every_post_info_returned["username_this_post_shared_from"] = every_shared_post["shared_from_username"]
                post_shared_to_you_list[every_shared_post_info["_id"]] = every_post_info_returned

        return jsonify({
            'success': True,
            'message': 'All shared post successfully displayed',
            "all_share_post_to_you_list": post_shared_to_you_list
        })

    else:
        return jsonify({
            'success': True,
            'message': 'log in to see your post others share to you',
            "all_share_post_to_you_list": post_shared_to_you_list
        })


@app.route("/dismiss_shared_post", methods=['POST', 'GET'])
def dismiss_shared_post():
    post_data = request.get_json()
    username_this_post_shared_from = post_data["username_this_post_shared_from"]
    current_user = post_data["current_user"]
    dismiss_shared_post_id = post_data["dismiss_shared_post_id"]
    user_collection.update(
        {"name": current_user},
        {"$pull":
             {"post_shared_to_you_list":
                  {"shared_post_id" : dismiss_shared_post_id,
                    "shared_from_username" : username_this_post_shared_from
                   }
              }
        }
    )

    user_collection.update(
        {"name": username_this_post_shared_from},
        {"$pull":
             {"post_you_share_to_other_list":
                  {"shared_post_id": dismiss_shared_post_id,
                   "shared_to_username": current_user
                   }
              }
         }
    )
    return jsonify({
        'success': True,
        'message': 'Dismiss shared post successfully'
    })


@app.route("/display_all_comment", methods=['POST', 'GET'])
def display_all_comment():
    post_data = request.get_json()
    post_id = post_data["postId"]
    current_user = post_data["current_user"]
    that_post = post_collection.find_one({"_id": ObjectId(post_id)})
    all_comments = []
    if that_post["all_comments"]:
        all_comments = that_post["all_comments"]
        return jsonify({
            'success': True,
            'message': 'Display all comments successfully',
            'all_comments': all_comments
        })
    else:
        return jsonify({
            'success': True,
            'message': 'Display all comments successfully',
            'all_comments': all_comments
        })


@app.route("/add_comment", methods=['POST', 'GET'])
def add_comment():
    post_data = request.get_json()
    post_id = post_data["postId"]
    current_user = post_data["current_user"]
    add_comment_content = post_data["add_comment_content"]
    # refer to https://stackoverflow.com/questions/10144852/how-can-i-create-unique-ids-for-embedded-documents-in-mongodb
    that_post = post_collection.update(
        {"_id": ObjectId(post_id)},
        {"$push":
            {"all_comments":
                {"_id": str(ObjectId()),
                "comment_creator": current_user,
                "comment_content": add_comment_content
                }
            }
        })

    return jsonify({
        'success': True,
        'message': 'Add comment successfully',
    })


@app.route("/delete_comment", methods=['POST', 'GET'])
def delete_comment():
    post_data = request.get_json()
    comment_id_to_delete = post_data["comment_id_to_delete"]
    post_id = post_data["post_id"]
    post_collection.update(
        {"_id": ObjectId(post_id)},
        {"$pull":
             {"all_comments": {
                 '_id' : comment_id_to_delete
             }}
        })

    return jsonify({
        'success': True,
        'message': 'Delete comment successfully',
    })

##88009
# @app.route('/')
# def hello_world():
#     dbfindresult = mongo.db.testdb.find()
#     for r in dbfindresult:
#         print(r['name'])
#     return "Hello world!"

if __name__ == '__main__':
    app.run()
