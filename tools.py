import json

DATA_FILE = "user_data.json"
current_user = None

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, 'w') as file:
            json.dump(data, file)
    except Exception as e:
        print(f"Error saving data: {e}")

def set_current_user(user):
    global current_user
    current_user = user

def get_current_user():
    global current_user
    return current_user

def create_user(username, password):
    data = load_data()
    data[username] = password
    data[username + "_flappy"] = 0
    data[username + "_tetris"] = 0
    data[username + "_snake"] = 0
    data[username + "_xo"] = 0
    save_data(data)
