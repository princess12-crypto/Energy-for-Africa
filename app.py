# Rebranded: Energy for Africa Admin Dashboard

# 📦 Imports
from flask import Flask, render_template, request, redirect, flash, url_for, session
import mysql.connector
from mysql.connector import pooling
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

# Create a MySQL connection pool to reuse connections efficiently
dbconfig = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "port": int(os.getenv("MYSQL_PORT", 3306)),
    "autocommit": True,
    "use_pure": True
}
connection_pool = pooling.MySQLConnectionPool(pool_name="mypool",
                                              pool_size=5,
                                              **dbconfig)

def get_mysql_connection():
    conn = connection_pool.get_connection()
    # Ping with reconnect True to avoid timeout disconnect
    conn.ping(reconnect=True, attempts=3, delay=2)
    return conn

def send_email(to_email, subject, content):
    smtp_server = os.getenv("BREVO_SMTP_SERVER")
    smtp_port = int(os.getenv("BREVO_SMTP_PORT", 587))
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
        traceback.print_exc()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, message))
        conn.commit()
    except mysql.connector.Error as err:
        print(f"❌ Failed to insert data into MySQL: {err}")
        traceback.print_exc()
        flash("An error occurred while submitting your message.")
        return redirect(url_for('home'))
    finally:
        cursor.close()
        conn.close()

    # Send confirmation email to user
    user_content = f"""
    <p>Hello {name},</p>
    <p>Thank you for contacting Energy for Africa. We received your message:</p>
    <blockquote>{message}</blockquote>
    <p>We will reply soon.</p>
    <p>— Energy for Africa Team</p>
    """
    send_email(email, "Message Received - Energy for Africa", user_content)

    # Notify admin
    admin_content = f"""
    <h3>New Contact Form Submission</h3>
    <p><strong>Name:</strong> {name}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Message:</strong> {message}</p>
    """
    send_email("celestinejustice4@gmail.com", "New Contact Form Message", admin_content)

    flash("Your message has been submitted successfully.")
    return redirect(url_for('home'))

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid login credentials")
            return redirect(url_for('admin_login'))
    return render_template('login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, message FROM contact_form ORDER BY id DESC")
        messages = cursor.fetchall()
    except Exception as e:
        print(f"❌ Error in /admin-dashboard: {e}")
        traceback.print_exc()
        return "❌ Failed to load admin dashboard."
    finally:
        cursor.close()
        conn.close()

    return render_template('admin.html', messages=messages)

@app.route('/reply', methods=['POST'])
def reply():
    if not session.get('admin_logged_in'):
        flash("You must be logged in to reply.")
        return redirect(url_for('admin_login'))

    to_email = request.form.get('to_email')
    reply_subject = request.form.get('reply_subject')
    reply_message = request.form.get('reply_message')

    try:
        send_email(to_email, reply_subject, reply_message)
        flash("Reply sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send reply: {e}")
        traceback.print_exc()
        flash("An error occurred while sending the reply.")

    return redirect(url_for('admin_dashboard'))

@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_message(message_id):
    if not session.get('admin_logged_in'):
        flash("You must be logged in to delete.")
        return redirect(url_for('admin_login'))

    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contact_form WHERE id = %s", (message_id,))
        conn.commit()
        flash("Message deleted successfully.")
    except Exception as e:
        print(f"❌ Failed to delete message: {e}")
        traceback.print_exc()
        flash("Failed to delete message.")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('admin_dashboard'))

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash("You have been logged out.")
    return redirect(url_for('admin_login'))

@app.route('/health')
def health():
    return "✅ App is running"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)