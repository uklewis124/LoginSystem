import sqlalchemy as sql
from password_encrypter import encrypt_password as encrypt

# WARNING: Database will be reset (even if this file is only imported). Check that RESET is set 
# to False before running this file.

RESET = False

def create_database():
    db = sql.create_engine('sqlite:///data.db')

    with db.connect() as conn:
        conn.execute(sql.text("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, name TEXT, username TEXT, email TEXT, hashed_password TEXT)"))
        conn.execute(sql.text(f"INSERT INTO data (name, username, email, hashed_password) VALUES ('Lewis', 'uklewis124', 'lewis@gmail.com', '{encrypt('Pa55w0rd')}')"))
        conn.commit()


if RESET:
    db = sql.create_engine('sqlite:///data.db')
    with db.connect() as conn:
        conn.execute(sql.text("DROP TABLE IF EXISTS data"))
        conn.commit()
    
    create_database()


def add_user(name, username, email, hashed_password):
    db = sql.create_engine('sqlite:///data.db')

    with db.connect() as conn:
        conn.execute(sql.text("INSERT INTO data (name, username, email, hashed_password) VALUES (:name, :username, :email, :hashed_password)"), 
                    {'name': name, 'username': username, 'email': email, 'hashed_password': hashed_password})
        conn.commit()

def remove_user(uid=None, username=None, hashed_password=None):
    if uid:
        db = sql.create_engine('sqlite:///data.db')

        with db.connect() as conn:
            conn.execute(sql.text("DELETE FROM data WHERE id = :id"), {'id': uid})
            conn.commit()
    
    elif username and hashed_password:
        # If username in database
        # If hashed password matches the hashed password in the database
        # Remove user
        
        db = sql.create_engine('sqlite:///data.db')
        
        with db.connect() as conn:
            target_user = conn.execute(sql.text("SELECT * FROM data WHERE username = :username AND hashed_password = :hashed_password"), {'username': username, 'hashed_password': hashed_password})
            if target_user:
                conn.execute(sql.text("DELETE FROM data WHERE username = :username AND hashed_password = :hashed_password"), {'username': username, 'hashed_password': hashed_password})
                conn.commit()
                return "User removed", 200
            else:
                return "User not found", 404
    else:
        return "Invalid request", 400


def select_user(uid=None, username=None, email=None):
    def select_user_search(uid=None, username=None, email=None):
        if uid:
            db = sql.create_engine('sqlite:///data.db')

            with db.connect() as conn:
                target_user = conn.execute(sql.text("SELECT * FROM data WHERE id = :id"), {'id': uid}).fetchone()
                return target_user
        
        elif username:
            db = sql.create_engine('sqlite:///data.db')

            with db.connect() as conn:
                target_user = conn.execute(sql.text("SELECT * FROM data WHERE username = :username"), {'username': username}).fetchone()
                return target_user

        elif email:
            db = sql.create_engine('sqlite:///data.db')

            with db.connect() as conn:
                target_user = conn.execute(sql.text("SELECT * FROM data WHERE email = :email"), {'email': email}).fetchone()
                return target_user

        else:
            return "Invalid request", 400
    
    selected_user = select_user_search(uid=uid, username=username, email=email)
    
    if selected_user:
        return selected_user, 200
    else:
        return "User not found", 404

def authenticate_user(username, hashed_password):
    db = sql.create_engine('sqlite:///data.db')

    with db.connect() as conn:
        target_user = conn.execute(sql.text("SELECT * FROM data WHERE username = :username AND hashed_password = :hashed_password"), {'username': username, 'hashed_password': hashed_password}).fetchone()
        
        if target_user:
            return "User authenticated", 200
        else:
            return "User not authorised", 401

def strip_user_data(user_data):
    return user_data[0][1], user_data[0][2], user_data[0][3]

def request_login():
    username = input("Enter username:").lower()
    password = encrypt(input("Enter password:"))
    
    result = authenticate_user(username, password)
    
    if result[1] == 200:
        user_data = {
            "name": None,
            "username": None,
            "email": None
        }
        
        selected_user = select_user(username=username)
        user_data["name"], user_data["username"], user_data["email"] = strip_user_data(selected_user)
        
        return user_data, 200
    else:
        return "Incorrect Login Details", 401

if __name__ == '__main__':
    create_database()
    
    user = request_login()
    
    if user[1] == 200:
        user = user[0]
        print(f"Welcome back, {user['name']}!")
    else:
        print(user[0])
