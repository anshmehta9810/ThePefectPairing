from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import secrets
secret_key = secrets.token_hex(16)
app = Flask(__name__)
app.secret_key = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLite database URI
db = SQLAlchemy(app)

# Define User and Companion models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    need = db.Column(db.String(100), nullable=False)
    interests = db.Column(db.String(255), nullable=False)
    max_price = db.Column(db.Float, nullable=False)

class Companion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_need = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    companion_id = db.Column(db.Integer, db.ForeignKey('companion.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, accepted, rejected

# Routes for rendering HTML templates
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Extract user data from the form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = int(request.form['age'])
        need = request.form['need']
        interests = ','.join(request.form.getlist('interests'))
        max_price = float(request.form['maxPrice'])

        # Create a new User object
        new_user = User(name=name, email=email, password=password, age=age, need=need, interests=interests, max_price=max_price)
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to user dashboard
        return redirect(url_for('user_dashboard'))

    return render_template('user_registration.html')

@app.route('/register/companion', methods=['GET', 'POST'])
def register_companion():
    if request.method == 'POST':
        # Extract companion data from the form
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        age = int(request.form['age'])
        address = request.form['address']

        # Create a new Companion object
        new_companion = Companion(name=name, email=email, password=password, age=age, address=address)
        # Add the new companion to the database
        db.session.add(new_companion)
        db.session.commit()

        # Redirect to companion dashboard
        return redirect(url_for('companion_dashboard'))

    return render_template('companion_registration.html')

@app.route('/login/user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user'] = user.id
            return redirect(url_for('user_dashboard'))
        else:
            return render_template('user_login.html', message='Invalid email or password.')

    return render_template('user_login.html')

@app.route('/login/companion', methods=['GET', 'POST'])
def login_companion():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        companion = Companion.query.filter_by(email=email, password=password).first()

        if companion:
            session['companion'] = companion.id
            return redirect(url_for('companion_dashboard'))
        else:
            return render_template('companion_login.html', message='Invalid email or password.')

    return render_template('companion_login.html')

@app.route('/user/dashboard')
def user_dashboard():
    if 'user' not in session:
        return redirect(url_for('login_user'))

    user_id = session['user']
    user = User.query.get(user_id)

    # Fetch recommended companions based on user preferences (replace with your recommendation logic)
    recommendations = Companion.query.filter(Companion.age.between(user.age - 5, user.age + 5),
                                            Companion.address.contains(user.need),
                                            Companion.max_price <= user.max_price).all()

    return render_template('user_dashboard.html', recommendations=recommendations)

@app.route('/companion/dashboard')
def companion_dashboard():
    if 'companion' not in session:
        return redirect(url_for('login_companion'))

    companion_id = session['companion']
    companion = Companion.query.get(companion_id)

    # Fetch received requests for the companion
    requests = Request.query.filter_by(companion_id=companion_id).all()

    return render_template('companion_dashboard.html', requests=requests)

if __name__ == '__main__':
    db.create_all()  # Create database tables based on models
    app.run(debug=True)
