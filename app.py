# 📦 Imports
from flask import Flask, render_template, request, redirect, flash, url_for, session  # ✅ session added
import mysql.connector
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
# 🔑 Load environment variables
load_dotenv()
# 🔐 Admin Login Credentials 👇
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")
print("✅ DEBUG: Loaded Admin Username:", ADMIN_USERNAME)
print("✅ DEBUG: Loaded Admin Password:", ADMIN_PASSWORD)
# 🚀 Flask app setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# 🧪 Debug MySQL
print("✅ DEBUG: Attempting to connect to MySQL with:")
print("HOST:", os.getenv("MYSQLHOST"))
print("PORT:", os.getenv("MYSQLPORT"))
print("USER:", os.getenv("MYSQLUSER"))
print("PASSWORD:", os.getenv("MYSQLPASSWORD"))
print("DATABASE:", os.getenv("MYSQLDATABASE"))
# 🔗 MySQL connection
try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL successfully")
except Exception as e:
    print(f"❌ Failed to connect to MySQL: {e}")
# ✉️ Send Email Function
def send_email(to_email, subject, content):
    smtp_server = os.getenv("BREVO_SMTP_SERVER")
    smtp_port = int(os.getenv("BREVO_SMTP_PORT"))
    smtp_user = os.getenv("BREVO_SMTP_USER")
    smtp_password = os.getenv("BREVO_SMTP_PASSWORD")
    from_email = os.getenv("FROM_EMAIL")
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(content, "html"))
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to_email, message.as_string())
        print(f"📨 Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")
# 🏠 Home Route
@app.route('/')
def home():
    return render_template('index.html')
# 📬 Submit Form Route
@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"📝 Form submitted: Name={name}, Email={email}, Message={message}")
    # 💾 Save to DB
    try:
        sql = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
        values = (name, email, message)
        cursor.execute(sql, values)
        conn.commit()
        print("✅ Form data inserted into database")
    except Exception as e:
        print(f"❌ Failed to insert data into MySQL: {e}")
    # 📧 Email to user
    user_content = f"""
    <p>Hello {name},</p>
    <p>Thank you for contacting TotalEnergies. We received your message:</p>
    <blockquote>{message}</blockquote>
    <p>We will reply soon.</p>
    <p>— TotalEnergies Nigeria</p>
    """
    send_email(email, "Message Received - TotalEnergies", user_content)
    # 📧 Email to admin
    admin_content = f"""
    <h3>New Contact Form Submission</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong> {message}</p>
    """
    send_email("celestinejustice4@gmail.com", "New Contact Form Message", admin_content)
    flash("Your message has been submitted successfully.")
    return redirect(url_for('home'))
# 🔐 Admin Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
         # ✅ Debug prints for login
        print("🔐 Submitted Username:", username)
        print("🔐 Submitted Password:", password)
        print("🔐 Expected Username:", ADMIN_USERNAME)
        print("🔐 Expected Password:", ADMIN_PASSWORD)
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash("Invalid login credentials")
            return redirect(url_for('login'))
    return render_template('login.html')
# 🧾 Admin Dashboard Route with Debugging
@app.route('/admin')
def admin():
    if not session.get('admin_logged_in'):
        print("🔒 Admin access denied. Redirecting to login.")
        return redirect(url_for('login'))
    print("📊 Admin logged in. Loading messages from database...")
    try:
        cursor.execute("SELECT name, email, message FROM contact_form ORDER BY id DESC")
        messages = cursor.fetchall()
        print(f"✅ Retrieved {len(messages)} messages from the database.")
        return render_template('admin.html', messages=messages)
    except Exception as e:
        print(f"❌ Error in /admin route: {e}")
        return "An error occurred while loading the admin dashboard."
# 🚪 Logout Route
@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))
# ▶️ Start App
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Flask app is starting...")
    app.run(host='0.0.0.0', port=port)
