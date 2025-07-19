from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
# Load environment variables from .env
load_dotenv()
# Flask app configuration
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# DEBUG: Print environment variables before MySQL connection
print("✅ DEBUG: Attempting to connect to MySQL with:")
print("HOST:", os.getenv("MYSQLHOST"))
print("PORT:", os.getenv("MYSQLPORT"))
print("USER:", os.getenv("MYSQLUSER"))
print("PASSWORD:", os.getenv("MYSQLPASSWORD"))
print("DATABASE:", os.getenv("MYSQLDATABASE"))
# MySQL Database connection setup
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
# Function to send email using Brevo SMTP
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
# Home route
@app.route('/')
def home():
    return render_template('index.html')
# Form submission route
@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    print(f"📝 Form submitted: Name={name}, Email={email}, Message={message}")
    # Save form to MySQL
    try:
        sql = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
        values = (name, email, message)
        cursor.execute(sql, values)
        conn.commit()
        print("✅ Form data inserted into database")
    except Exception as e:
        print(f"❌ Failed to insert data into MySQL: {e}")
    # Email to user
    user_content = f"""
    <p>Hello {name},</p>
    <p>Thank you for contacting TotalEnergies. We received your message:</p>
    <blockquote>{message}</blockquote>
    <p>We will reply soon.</p>
    <p>— TotalEnergies Nigeria</p>
    """
    send_email(email, "Message Received - TotalEnergies", user_content)
    # Email to admin
    admin_content = f"""
    <h3>New Contact Form Submission</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong> {message}</p>
    """
    send_email("celestinejustice4@gmail.com", "New Contact Form Message", admin_content)
    flash("Your message has been submitted successfully.")
    return redirect(url_for('home'))
# Start the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print("🚀 Flask app is starting...")
    app.run(host='0.0.0.0', port=port)