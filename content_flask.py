from flask import Flask, render_template_string, request, redirect, url_for
import csv
import os
from datetime import datetime

app = Flask(__name__)

CSV_FILE = "responses.csv"

# Ensure CSV file exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Name", "Age Range", "Email", "Password", "Awareness Level"])


HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Cybersecurity Awareness Survey</title>
    <style>
        body { font-family: Arial; background: #f4f6f8; }
        .container {
            width: 400px; margin: 60px auto; background: white;
            padding: 20px; border-radius: 10px; box-shadow: 0 0 10px #ccc;
        }
        h2 { text-align: center; }
        input, select { width: 100%; padding: 8px; margin: 8px 0; }
        button {
            width: 100%; padding: 10px; background: #007bff;
            color: white; border: none; border-radius: 5px;
        }
        .notice {
            font-size: 12px; color: #555; margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Cybersecurity Awareness Survey</h2>

        <p class="notice">
        This is an educational demo form. Your information is collected only
        for learning purposes with your consent.
        </p>

        <form method="POST" action="/submit">
            <label>Name (optional)</label>
            <input type="text" name="name">

            <label>Age Range</label>
            <select name="age" required>
                <option value="">Select</option>
                <option>Below 18</option>
                <option>18-25</option>
                <option>26-40</option>
                <option>40+</option>
            </select>

            <label>Email </label>
            <input type="email" name="email">
            <label>Password </label>
            <input type="password" name="password">
            <label>How aware are you about phishing attacks?</label>
            <select name="awareness" required>
                <option value="">Select</option>
                <option>Not aware</option>
                <option>Somewhat aware</option>
                <option>Very aware</option>
            </select>

            <label>
                <input type="checkbox" name="consent" required>
                I agree to provide this information for educational purposes.
            </label>

            <button type="submit">Submit</button>
        </form>
    </div>
</body>
</html>
"""


HTML_THANKS = """
<!DOCTYPE html>
<html>
<head>
    <title>Thank You</title>
</head>
<body style="font-family: Arial; text-align:center; margin-top:100px;">
    <h2>Thank you for participating!</h2>
    <p>Your response has been recorded for educational purposes.</p>
    <a href="/">Go back</a>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_FORM)


@app.route("/submit", methods=["POST"])
def submit():
    if "consent" not in request.form:
        return "Consent is required.", 400

    name = request.form.get("name", "")
    age = request.form.get("age", "")
    email = request.form.get("email", "")
    password = request.form.get("password", "")
    awareness = request.form.get("awareness", "")

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name,
            age,
            email,
            password,
            awareness,
        ])

    return render_template_string(HTML_THANKS)


if __name__ == "__main__":
    app.run(debug=True)
