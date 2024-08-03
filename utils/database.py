user_points = {}
user_missions = {}  # New dictionary to store user missions

def update_points(user_id, points):
    user_points[user_id] = user_points.get(user_id, 0) + points

def get_user_points(user_id):
    points = user_points.get(user_id, 0)
    sorted_users = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
    rank = next((i for i, (id, _) in enumerate(sorted_users) if id == user_id), -1) + 1
    return points, rank

def get_top_users(limit):
    return sorted(user_points.items(), key=lambda x: x[1], reverse=True)[:limit]

# New functions

def get_user_missions(user_id):
    return user_missions.get(user_id, [])

def complete_mission(user_id, mission_id):
    if user_id not in user_missions:
        user_missions[user_id] = []
    if mission_id not in user_missions[user_id]:
        user_missions[user_id].append(mission_id)
        return True
    return False