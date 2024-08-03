from pymongo import MongoClient
import os

# MongoDB setup
MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['mohamed051']

# Collections
users = db['users']
missions = db['missions']
questions = db['questions']

def update_points(user_id, points):
    print(f"Updating points for user {user_id}: {points}")
    users.update_one({'_id': user_id}, {'$inc': {'points': points}}, upsert=True)

def get_user_points(user_id):
    print(f"Getting points for user {user_id}")
    user = users.find_one({'_id': user_id})
    points = user['points'] if user and 'points' in user else 0
    rank = users.count_documents({'points': {'$gt': points}}) + 1
    return points, rank

def get_top_users(limit):
    print(f"Getting top {limit} users")
    return list(users.find().sort('points', -1).limit(limit))

def get_user_missions(user_id):
    print(f"Getting missions for user {user_id}")
    user = users.find_one({'_id': user_id})
    return user.get('completed_missions', []) if user else []

def complete_mission(user_id, mission):
    print(f"Completing mission for user {user_id}: {mission}")
    result = users.update_one(
        {'_id': user_id},
        {'$addToSet': {'completed_missions': mission}},
        upsert=True
    )
    return result.modified_count > 0

def add_mission(description, points):
    print(f"Adding mission: {description}, {points} points")
    missions.insert_one({'description': description, 'points': points})

def get_all_missions():
    print("Getting all missions")
    return list(missions.find())

def add_question(question, answer, points):
    print(f"Adding question: {question}")
    questions.insert_one({'question': question, 'answer': answer, 'points': points})

def get_all_questions():
    print("Getting all questions")
    return list(questions.find())

def remove_question(index):
    print(f"Removing question at index {index}")
    all_questions = list(questions.find())
    if 0 <= index < len(all_questions):
        question_to_remove = all_questions[index]
        questions.delete_one({'_id': question_to_remove['_id']})
        return True
    return False