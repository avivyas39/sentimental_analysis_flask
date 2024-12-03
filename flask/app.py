import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from train import analyze_sentiment  # Import the function from train.py

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# User Model (same as before)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
 
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# Create database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session["user_id"] = user.id
            return redirect(url_for("sentiment"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return "User already exists. Please log in."

        new_user = User(name, email, password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/sentiment", methods=["GET", "POST"])
def sentiment():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        if 'file' not in request.files:
            return "No file part in the request."
        file = request.files['file']

        if file.filename == '':
            return "No selected file."

        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            try:
                # Call the function from train.py
                df, plot_path = analyze_sentiment(filepath, app.config['UPLOAD_FOLDER'])

                return render_template(
                    "sentiment.html",
                    tables=[df.to_html(classes='data', index=False)],
                    plot_url=url_for('static', filename=f'uploads/{os.path.basename(plot_path)}')
                )
            except ValueError as e:
                return str(e)
        else:
            return "Invalid file format. Please upload a CSV file."
    return render_template("sentiment.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
