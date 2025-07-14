from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Heroku workaround for SQLAlchemy postgres URL
if os.getenv("DATABASE_URL", "").startswith("postgres://"):
    os.environ["DATABASE_URL"] = os.environ["DATABASE_URL"].replace("postgres://", "postgresql://", 1)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///weight_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(512), unique=True, nullable=False)
    password_hash = db.Column(db.String(512), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        weight = float(request.form['weight'])
        entry = WeightEntry.query.filter_by(user_id=current_user.id, date=date).first()
        if entry:
            entry.weight = weight
        else:
            entry = WeightEntry(date=date, weight=weight, user_id=current_user.id)
            db.session.add(entry)
        db.session.commit()

    entries = WeightEntry.query.filter_by(user_id=current_user.id).order_by(WeightEntry.date).all()
    data = [(e.date, e.weight) for e in entries]
    df = pd.DataFrame(data, columns=['Date', 'Weight'])

    plot_url = None
    if not df.empty:
        img = io.BytesIO()
        plt.figure(figsize=(8, 4))
        plt.plot(df['Date'], df['Weight'], marker='o')
        plt.title('Weight Progress')
        plt.xlabel('Date')
        plt.ylabel('Weight')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', plot_url=plot_url, data=data)

if __name__ == '__main__':
    app.run(debug=True)
