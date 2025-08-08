# 🏋️‍♀️ Weight Tracker App

A simple web application to log daily weight, visualize progress, and stay on track — built with **Flask**, **SQLAlchemy**, **Heroku**, and **Matplotlib**.

Live demo: [https://weight-tracker-app.herokuapp.com](https://weight-tracker-app-bd46e6bcd775.herokuapp.com/login?next=%2F)

---

## 📊 Features

- 📅 Log your daily weight entries
- 📈 Visualize progress with real-time plots
- 👤 User authentication (register, log in, log out)
- 🗂️ Data stored securely using PostgreSQL
- 🌐 Deployed on Heroku — accessible from anywhere

---

## 🛠️ Tech Stack

- **Backend**: Flask, SQLAlchemy, Flask-Migrate, Flask-Login
- **Database**: PostgreSQL (Heroku Add-on)
- **Frontend**: HTML (Jinja2 templates), Bootstrap
- **Visualization**: Matplotlib
- **Deployment**: Heroku + Gunicorn

---

## 🚀 Getting Started Locally

### 1. Clone the repository

```bash
git clone https://github.com/tshekar9/weight-tracker-app.git
cd weight-tracker-app
```

### 2. Set up a virtual environment

```bash
python3 -m venv weight_tracker_env
source weight_tracker_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set environment variables

```bash
Create a .env file with:

FLASK_APP=app.py
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///weight_data.db  # for local testing
```

### 5. Initialize the database

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Run the app

```bash
flask run
```

### ☁️ Deploying to Heroku

Make sure you have the Heroku CLI installed and logged in.

```bash
heroku create weight-tracker-app
heroku addons:create heroku-postgresql
git push heroku main
heroku run flask db upgrade
heroku open
```

### 📌 Folder Structure

├── app.py
├── templates/
│   └── (HTML files)
├── migrations/
├── instance/
│   └── weight_data.db (local)
├── requirements.txt
├── Procfile
└── .python-version

### 🙋‍♀️ Author

Tejaswini Shekar
[GitHub](https://github.com/tshekar9)

### ⭐ Future Improvements

- Add user dashboards with BMI and goal tracking.
- Feature to allow export of data to CSV.
- Email reminders or push notifications to track daily.

### 📝 License

This project is open-source and available under the MIT License.
