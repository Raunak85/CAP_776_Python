import csv
import hashlib
import re
import requests
import datetime
import getpass  

API_KEY = "1XpSa6mhdNq0IhdvHBeUe0zHyLLqs2QN3q6kF4YI"
CSV_FILE = "regno.csv"
ACTIVITY_LOG = "user_activity_log.log"
MAX_ATTEMPTS = 5

def log_user_activity(email, action):  # for storing user activity
    with open(ACTIVITY_LOG, mode='a') as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {email} - {action}\n")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    return len(password) >= 8 and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)

def read_csv():
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def write_csv(users):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['email', 'password', 'security_question', 'security_answer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(users)

# Signup function
def signup():
    users = read_csv()
    email = input("Enter your email: ")

    if not validate_email(email):
        print("Invalid email format.")
        return

    for user in users:
        if user['email'] == email:
            print("Email already registered.")
            return

    password = getpass.getpass("Enter your password (min 8 characters, 1 special character): ")  

    if not validate_password(password):
        print("Password does not meet the criteria.")
        return
        
    confirm_password = input("Confirm your password (visible): ")

    if password != confirm_password:
        print("Passwords do not match. Please try again.")
        return

    hashed_password = hash_password(password)
    security_question = input("Enter your security question (e.g., Your first pet's name): ")
    security_answer = input("Enter the answer: ")
    hashed_answer = hash_password(security_answer)

    new_user = {
        'email': email,
        'password': hashed_password,
        'security_question': security_question,
        'security_answer': hashed_answer
    }

    users.append(new_user)
    write_csv(users)
    log_user_activity(email, "Signup")
    print("Signup successful!")

# Login function with up to 5 attempts
def login():
    users = read_csv()
    attempts = 0

    while attempts < MAX_ATTEMPTS:
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")  

        hashed_password = hash_password(password)

        for user in users:
            if user['email'] == email and user['password'] == hashed_password:
                log_user_activity(email, "Login")
                print("Login successful!")
                return email

        attempts += 1
        print(f"Invalid credentials. Attempts left: {MAX_ATTEMPTS - attempts}")

    print("Too many failed attempts. Try again later.")
    return None

# Forgot Password function
def forgot_password():
    users = read_csv()
    email = input("Enter your registered email: ")

    for user in users:
        if user['email'] == email:
            print(f"Security Question: {user['security_question']}")
            answer = input("Enter your answer: ")

            if hash_password(answer) == user['security_answer']:
                new_password = getpass.getpass("Enter a new password (min 8 characters, 1 special character): ")  # Masked password input

                if validate_password(new_password):
                    user['password'] = hash_password(new_password)
                    write_csv(users)
                    log_user_activity(email, "Password Reset")
                    print("-----------------------------")
                    print("Password reset successful!")
                    print("-----------------------------")
                else:
                    print("Password does not meet criteria.")
                return
            else:
                print("Incorrect security answer.")
                return

    print("Email not found.")

def get_neo_data(email):
    print("Fetching Near Earth Object data...")
    url = f"https://api.nasa.gov/neo/rest/v1/feed?api_key={API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        for date in data['near_earth_objects']:
            for neo in data['near_earth_objects'][date]:
                print(f"Name: {neo['name']}, Close approach date: {neo['close_approach_data'][0]['close_approach_date']}")
                print(f"Estimated diameter (meters): {neo['estimated_diameter']['meters']['estimated_diameter_max']}")
                print(f"Velocity (km/h): {neo['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']}")
                print(f"Miss distance (km): {neo['close_approach_data'][0]['miss_distance']['kilometers']}")
                print(f"Hazardous: {neo['is_potentially_hazardous_asteroid']}")
                print("-" * 40)
        log_user_activity(email, "Fetched NEO Data")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

# display Solar System Dynamics (SSD) data from NASA API
def get_ssd_data(email):
    print("Fetching Solar System Dynamics (SSD) data...")
    url = "https://ssd-api.jpl.nasa.gov/cad.api"
    
    try:
        response = requests.get(url)
        data = response.json()

        if 'data' in data:
            headers = ['Object Name', 'Close Approach Date', 'Miss Distance (km)', 'Velocity (km/s)', 'Magnitude']
            print(f"{headers[0]:<20} {headers[1]:<20} {headers[2]:<25} {headers[3]:<20} {headers[4]:<10}")
            print("-" * 95)
            
            for item in data['data']:
                object_name = item[0] 
                close_approach_date = item[3]  
                miss_distance_km = item[4]  
                velocity_kms = item[7]
                magnitude = item[10]  
                
                print(f"{object_name:<20} {close_approach_date:<20} {miss_distance_km:<25} {velocity_kms:<20} {magnitude:<10}")
            
            log_user_activity(email, "Fetched SSD Data")
        else:
            print("No data found.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
# Main function
def main():
    print("\n***************Welcome to NASA Space Data Access*********")

    while True:
        print("\n1. Sign Up")
        print("\n2. Login")
        print("\n3. Forgot Password")
        print("\n4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == '1':
            signup()

        elif choice == '2':
            email = login()
            if email:
                while True:
                    print("\n--- API Options ---")
                    print("1. Near Earth Object (NEO)")
                    print("2. Solar System Dynamics (SSD)")
                    print("3. Logout")

                    api_choice = input("Enter your choice: ")

                    if api_choice == '1':
                        get_neo_data(email)
                    elif api_choice == '2':
                        get_ssd_data(email)
                    elif api_choice == '3':
                        log_user_activity(email, "Logout")
                        print("Logged out.")
                        break
                    else:
                        print("Invalid option. Try again.")

        elif choice == '3':
            forgot_password()

        elif choice == '4':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
