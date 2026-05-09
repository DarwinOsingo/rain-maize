import datetime
import getpass

# Database with users, passwords, and roles
USERS = {
    "catherine": {
        "password": "pass254",
        "role": "ADMINISTRATOR"
    },
    "claire": {
        "password": "mypassword",
        "role": "student"
    }
}

def display_banner():
    """Display a welcome banner at the start"""
    print("=" * 50)
    print("      WELCOME TO BBIT LOGIN PORTAL")
    print("=" * 50)

def get_credentials():
    """Prompts user for input and masks the password."""
    print("\nPlease enter your login details")
    username = input("Username: ").strip().lower()
    password = getpass.getpass("Enter password: ").strip()
    return username, password

def validate_input(username, password):
    """Returns True if both username and password are provided"""
    if not username or not password:
        print("Invalid username or password. Please try again.")
        return False
    return True

def authenticate(username, password):
    """Check if the username and password match the database."""
    user_record = USERS.get(username)
    if user_record is None:
        return False
    return user_record["password"] == password

def lock_failed_attempt(attempts, max_attempts):
    """Handles lockout logic with timestamping."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remaining = max_attempts - attempts

    print(f"[{timestamp}] AUTH FAILURE: Attempt {attempts} of {max_attempts}.")
    if remaining > 0:
        print(f">> Access Denied. {remaining} attempts remaining.")
    else:
        print("\n" + "!" * 45)
        print(f"[{timestamp}] SECURITY CRITICAL: SYSTEM LOCKOUT")
        print("!" * 45)

def display_results(success, username=None):
    """Display the login attempt result."""
    print()
    if success and username in USERS:
        role = USERS[username]["role"]
        print("=" * 50)
        print(f"Login successful! Welcome, {username}.")
        print(f"Role: {role}")
        print("=" * 50)
    else:
        print("Login unsuccessful. Please try again later.")

def main():
    """Main program flow control."""
    display_banner()

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
        username, password = get_credentials()

        # Validate input
        if not validate_input(username, password):
            continue

        # Authenticate
        if authenticate(username, password):
            display_results(True, username)
            return
        else:
            attempts += 1
            lock_failed_attempt(attempts, max_attempts)

    # Lockout after max attempts
    display_results(False)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting cleanly.")
        print("\n Goodbye")
