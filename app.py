from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename 
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configure SQL Alchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder to store uploaded images

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15))
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    venue = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.String(200), nullable=True)
    
    club = db.relationship('Club', backref=db.backref('events', lazy=True))

class Event_Reg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), db.ForeignKey('user.username'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)

    # Define the relationship between User and Event models
    user = db.relationship('User', backref=db.backref('registered_events', lazy=True))
    event = db.relationship('Event', backref=db.backref('registrations', lazy=True))



# Route to render add_admin page
@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        current_admin_password = request.form['currentAdminPassword']

        # Check if the password and confirm password match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('add_admin'))

        # Fetch the current session admin to check the password
        current_admin = Admin.query.filter_by(username=session.get('username')).first()

        if not current_admin or not current_admin.check_password(current_admin_password):
            flash('Authorization failed! Incorrect current password.', 'error')
            return redirect(url_for('add_admin'))

        # Add new admin to the database
        new_admin = Admin(username=username)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()

        flash('New admin added successfully!', 'success')
        return redirect(url_for('home'))

    return render_template('add_admin.html', username=session['username'])

@app.route('/verify_admin_password', methods=['POST'])
def verify_admin_password():
    data = request.get_json()
    current_password = data.get('password')

    current_admin = Admin.query.filter_by(username=session.get('username')).first()

    if current_admin and current_admin.check_password(current_password):
        return {"success": True}
    else:
        return {"success": False}, 400


# @app.route('/authorize_admin', methods=['POST'])
# def authorize_admin():
#     current_session_password = session.get('admin_password')  

#     if not current_session_password:
#         return jsonify({'status': 'error', 'message': 'Session not found'}), 403


#     entered_password = request.json.get('password')

#     if check_password_hash(current_session_password, entered_password):  
#         return jsonify({'status': 'success', 'message': 'Authorization successful'})
#     else:
#         return jsonify({'status': 'error', 'message': 'Authorization failed'}), 403


# Route to display the login selection page
@app.route("/")
def login():
    if "username" in session:
        return redirect(url_for('home'))
    return render_template("login.html")

# Route to handle login submission for Admin and Student
@app.route("/login", methods=["POST"])
def login_post():
    role = request.form['role']
    username = request.form['username']
    password = request.form['password']

    # Login for admin using Admin model
    if role == "admin":
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['username'] = username
            session['role'] = role
            return redirect(url_for('home'))

    # Dynamic login for students
    if role == "student":
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            session['role'] = role
            return redirect(url_for('home'))

    flash("Invalid login credentials.")
    return redirect(url_for('login'))

# Route to handle registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        age = request.form['age']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        mobile = request.form['mobile']

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash("User already exists!")
            return redirect(url_for('register'))

        new_user = User(name=name, age=age, username=username, email=email, mobile=mobile, role="student")
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        session['role'] = "student"
        return redirect(url_for('home'))

    return render_template("register.html")



from datetime import datetime

@app.route('/add_event', methods=['GET', 'POST'])
def addevent():
    if request.method == 'POST':
        # Retrieve form data
        event_name = request.form['event_name']
        event_description = request.form['event_description']
        club_name = request.form['club_name']
        event_date_str = request.form['event_date']  # String format from form input
        event_time_str = request.form['event_time']  # String format from form input
        venue = request.form['venue']
        price = int(request.form['price'])
        num_people = int(request.form['num_people'])

        # Convert date and time strings to date and time objects
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
        event_time = datetime.strptime(event_time_str, '%H:%M').time()

        # Handle the poster file upload
        poster = request.files['poster']
        if poster:
            filename = secure_filename(poster.filename)
            poster_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            poster.save(poster_path)

        # Retrieve or create the club
        club = Club.query.filter_by(name=club_name).first()
        if not club:
            club = Club(name=club_name)
            db.session.add(club)
            db.session.commit()

        # Create a new Event instance
        new_event = Event(
            name=event_name,
            description=event_description,
            club_id=club.id,
            date=event_date,  # Now a date object
            time=event_time,  # Now a time object
            venue=venue,
            price=price,
            num_people=num_people,
            poster=poster_path
        )
        db.session.add(new_event)
        db.session.commit()

        flash("Event successfully added!")
        return redirect(url_for('addevent'))

    # GET method: Show form
    clubs = Club.query.all()
    return render_template('add_event.html', clubs=clubs)



@app.route("/home")
def home():
    if "username" not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(username=session['username']).first()
    if user and session['role'] == 'student':
        # Student view: Display events available for registration
        events = Event.query.all()
        clubs_with_events = (
            db.session.query(Club)
            .join(Event, Club.id == Event.club_id)
            .distinct(Club.name)
            .all()
        )
        clubs_with_events_data = [
            {"club": club, "events": Event.query.filter_by(club_id=club.id).all()}
            for club in clubs_with_events
        ]
        return render_template("student_home.html", user_id=user.id, username=user.username, name=user.name, role=user.role, 
                               events=events, clubs_with_events=clubs_with_events_data)

    elif session['role'] == 'admin':
        # Admin view: Display club-specific events
        admin = Admin.query.filter_by(username=session['username']).first()
        clubs_with_events = (
            db.session.query(Club)
            .join(Event, Club.id == Event.club_id)
            .distinct(Club.name)
            .all()
        )
        clubs_with_events_data = [
            {"club": club, "events": Event.query.filter_by(club_id=club.id).all()}
            for club in clubs_with_events
        ]
        return render_template("admin_home.html", username=admin.username, events=Event.query.all(), 
                               clubs_with_events=clubs_with_events_data)
    else:
        flash("Invalid session.")
        return redirect(url_for('login'))

@app.route('/register_event', methods=['POST'])
def register_event():
    event_id = request.form.get('event_id')
    username = request.form.get('username')
    
    # Check if the user is already registered for the event
    existing_registration = Event_Reg.query.filter_by(username=username, event_id=event_id).first()
    if existing_registration:
        flash("You are already registered for this event.", "danger")
        return redirect(url_for('home'))  # Redirect to the same page if already registered
    
    # Create new registration
    registration = Event_Reg(username=username, event_id=event_id)
    db.session.add(registration)
    db.session.commit()
    
    flash("Registration successful!", "success")  # Success message after registration
    return redirect(url_for('home'))  # Redirect to the student's home page after registration

# @app.route('/registered_events')
@app.route('/registered_events')
def registered_events():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in
    
    username = session['username']
    user = User.query.filter_by(username=username).first()
    
    # Fetch registered events for the logged-in user
    registered_events = Event_Reg.query.filter_by(username=username).all()
    
    # Create a list of event IDs based on the registrations
    event_id = [Event_Reg.event_id for reg in registered_events]
    
    # Fetch the events from the Event table based on the event IDs
    events = Event.query.filter(Event.id.in_(event_id)).all()
    
    # Pass the events to the template
    return render_template('registered_events.html', events=events, user_id=user.id, username=user.name, role=user.role)



# Route for updating profile
@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "username" in session:
        user = User.query.filter_by(username=session['username']).first()
        if request.method == "POST":
            user.name = request.form['name']
            user.age = request.form['age']
            user.email = request.form['email']
            user.mobile = request.form['mobile']
            db.session.commit()
            flash("Profile updated successfully!")
            return redirect(url_for('profile'))
        
        return render_template("profile.html", user=user)
    return redirect(url_for('login'))

# Route for changing password
@app.route("/change_password", methods=["POST"])
def change_password():
    if "username" in session:
        user = User.query.filter_by(username=session['username']).first()
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        if not user.check_password(old_password):
            flash("Old password is incorrect!")
        elif new_password != confirm_new_password:
            flash("New passwords do not match!")
        else:
            user.set_password(new_password)
            db.session.commit()
            flash("Password updated successfully!")
        return redirect(url_for('profile'))
    return redirect(url_for('login'))

# Route for logging out
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/admin_home")
def adminhome():
    if "username" in session and session['role'] == 'admin':
        admin = Admin.query.filter_by(username=session['username']).first()

        # Get distinct clubs with events
        clubs_with_events = (
            db.session.query(Club)
            .join(Event, Club.id == Event.club_id)
            .distinct(Club.name)
            .all()
        )

        # Fetch each club with its events
        clubs_with_events_data = [
            {"club": club, "events": Event.query.filter_by(club_id=club.id).all()}
            for club in clubs_with_events
        ]

        return render_template("admin_home.html", username=admin.username.capitalize(), clubs_with_events=clubs_with_events_data)
    return redirect(url_for('login'))


# Route to get event details for editing
@app.route("/get_event/<int:event_id>")
def get_event(event_id):
    event = Event.query.get(event_id)
    if event:
        return jsonify({
            "id": event.id,
            "name": event.name,
            "description": event.description,
            "date": event.date.isoformat(),
            "time": event.time.isoformat(),
            "venue": event.venue,
            "price": event.price,
            "num_people": event.num_people
        })
    return jsonify({"error": "Event not found"}), 404

from datetime import datetime

@app.route("/edit_event", methods=["POST"])
def edit_event():
    data = request.get_json()
    event = Event.query.get(data['id'])
    
    if event:
        # Convert the string date and time to Python date and time objects
        try:
            event.name = data['name']
            event.description = data['description']
            
            # Convert string date to datetime.date object
            event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            
            # Convert string time to datetime.time object
            event.time = datetime.strptime(data['time'], '%H:%M:%S').time()
            
            event.venue = data['venue']
            event.price = data['price']
            event.num_people = data['num_people']
            
            db.session.commit()
            return jsonify({"success": True})
        except ValueError as e:
            return jsonify({"error": f"Invalid date or time format: {str(e)}"}), 400
    
    return jsonify({"error": "Event not found"}), 404


# Route to handle event deletion
@app.route("/delete_event/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        Event_Reg.query.filter_by(event_id=event_id).delete()
        db.session.delete(event)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"error": "Event not found"}), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
