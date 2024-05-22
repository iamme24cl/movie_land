import requests
import csv

def fetch_users_and_seed():
    r = requests.get("https://randomuser.me/api/?results=610")
    print(f"status code {r.status_code}")
    json_data = r.json() 
    users = []
    user_id = 1

    # The 'results' key contains the list of user data.
    for user in json_data['results']:
        u = {
            "id": user_id,
            "first_name": user['name']['first'],
            "last_name": user['name']['last'],
            "email": user['email'],
            "password": user['login']['password'],
            "avatar": user['picture']['thumbnail']
        }
        users.append(u)
        user_id += 1

    print(f"length of users --> {len(users)}")
    headers = users[0].keys()
    with open("data/users.csv", "w", newline="\n") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(users)
    
if __name__ == "__main__":
    fetch_users_and_seed()
