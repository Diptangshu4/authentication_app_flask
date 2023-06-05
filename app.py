from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secret key of your choice

# Mock database
users = []

# Home page
@app.route("/")
def home():
    if 'username' in session:
        return render_template("home.html", username=session['username'])
    return render_template("index.html")

# User registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        # Check if username already exists
        if any(user['username'] == username for user in users):
            return render_template("register.html", error="Username already exists")

        user = {'username': username, 'password': hashed_password}
        users.append(user)
        return redirect(url_for('login'))

    return render_template("register.html")

# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Find the user in the database
        user = next((user for user in users if user['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('home'))

        return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")

# User logout
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Profile page
@app.route("/profile")
def profile():
    if 'username' in session:
        return render_template("profile.html", username=session['username'])
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
