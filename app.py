from flask import Flask, render_template, request, redirect, flash, url_for
import mysql.connector
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os 
# Load environment variables
load_dotenv()
# Flask app config
app = Flask(__name__)
app.secret_key = 'a3d892249e2d0ecb3c11cd477cc2fa10' # Required for flashing messages 
# MySQL Database connection setup
conn = mysql.connector.connect(
    host="localhost",   
    user="root",
    password="Total@2025!",
    database="totalenergies_db"
)
cursor = conn.cursor()
# Function to send email using Brevo SMTP
def send_email(to_email, subject, content):
     # Load SMTP server from environment
     smtp_server = os.getenv("BREVO_SMTP_SERVER")
     # Load SMTP port from environment, and cast to integer 
     smtp_port = int(os.getenv("BREVO_SMTP_PORT"))
     # Load SMTP user from environment
     smtp_user = os.getenv("BREVO_SMTP_USER")
     # Load SMTP password from environment
     smtp_password = os.getenv("BREVO_SMTP_PASSWORD") # Load from .env
     message = MIMEMultipart()
     # Load your FROM email from environment
     message["From"] = os.getenv("FROM_EMAIL")
     message["To"] = to_email
     message["Subject"] = subject
     message.attach(MIMEText(content, "html"))
     try:
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls(context=context)
            server.login(smtp_user, smtp_password)
            server.sendmail(message["From"], to_email, message.as_string())
        print(f"Email sent successfully to {to_email}")
     except Exception as e:
        print(f"Failed to send email: {e}")
# Home route
@app.route('/')
def home():
    return render_template('index.html') 
# Form submission route
@app.route('/submit-form', methods=['POST'])
def submit_form():
     name = request.form.get('name')
     email = request.form.get('email')
     user_message = request.form.get('message')
     # Print to console for testing
     print(f"Name: {name}, Email: {email}, Message: {user_message}")
     # Insert data into MySQL
     sql = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
     values = (name, email, user_message)
     cursor.execute(sql, values)
     conn.commit()
     # Send confirmation email to user 
     user_email_content = f"""
     <p>Hi {name},</p>
     <p>Thank you for reaching out to TotalEnergies. We have received your message:</p>
     <blockquote>{user_message}</blockquote>
     <p>Our team will get back to you as soon as possible.</p>
     <p>Best regards,<br>TotalEnergies Nigeria</p>
     """
     send_email(email, "Thanks for contacting TotalEnergies", user_email_content)
     # Notify admin
     admin_email_content = f"""
     <h3>New Contact Form Submission:</h3>
     <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Message:</b> {user_message}</p>
    """
     send_email("celestinejustice4@gmail.com", "New Contact Form Submission", admin_email_content)
     flash("Your message has been received. Thank you!")
     return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
     