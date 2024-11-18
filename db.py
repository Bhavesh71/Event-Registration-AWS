from app import app, db, Admin  # Ensure 'app' is imported

def add_admin(username, password):
    admin = Admin(username=username)
    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()
    print("Admin user added successfully.")

if __name__ == "__main__":
    admin_username = "admin"  # Change as needed
    admin_password = "admin123"  # Change as needed

    with app.app_context():
        add_admin(admin_username, admin_password)
