import requests

# Configuration
BASE_URL = "http://localhost:8000/signup"
HEADERS = {
    "Content-Type": "application/json"
}

# Sample user data with specific usernames
USERS = [
    {"username": "sean", "password": "password0"},
    {"username": "jadon", "password": "password1"},
    {"username": "craig", "password": "password2"},
    {"username": "jen", "password": "password3"},
    {"username": "bri", "password": "password4"},
    {"username": "stacy", "password": "password5"},
    {"username": "becky", "password": "password6"},
    {"username": "kiesha", "password": "password7"},
    {"username": "ashley", "password": "password8"},
    {"username": "dani", "password": "password9"}
]

# Function to seed users
def seed_users():
    for user in USERS:
        response = requests.post(BASE_URL, json=user, headers=HEADERS)
        if response.status_code == 200 or response.status_code == 201:
            print(f"Created {user['username']} with ID: {response.json()['user']['id']}")
        else:
            print(f"Failed to create {user['username']}: {response.status_code} - {response.text}")

# Run the seeding
if __name__ == "__main__":
    seed_users()