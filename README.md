# ⚡ Energy for Africa – Web App (Flask + MySQL)

**Energy for Africa** is a modern web platform built to promote awareness, innovation, and collaboration around sustainable energy solutions across the African continent.

> Built with Flask, MySQL, and deployed via [Railway](https://railway.app)

---

## 🌍 Features

- ✅ Responsive and engaging landing page
- ✅ Dynamic contact form with email + database integration
- ✅ Admin dashboard to view submitted form data
- ✅ Scroll-triggered animations & mobile optimization
- ✅ Rebranded from TotalEnergies to support African energy initiatives

---

## 🚀 Live Demo

🔗 [Visit Energy for Africa Live](https://web-production-76476.up.railway.app)

---

## 💡 Why this Project?

Access to clean, affordable energy remains a major challenge across Africa. This platform:

- Serves as an **informational hub** on energy topics
- Acts as a **call-to-action** for sustainable development
- Demonstrates **full-stack web development** in action

---

## 📦 Tech Stack

| Frontend       | Backend       | Database | Deployment |
|----------------|---------------|----------|------------|
| HTML, CSS, JS  | Flask (Python)| MySQL    | Railway    |

---

## 🛠️ Setup & Deployment

### 🔗 One-Click Deploy (via Railway)

[![Deploy on Railway](https://railway.com/button.svg)](https://railway.com/deploy/72KWGM?referralCode=yi_Rfl)

> Use the button above to clone and deploy this project on Railway instantly.

---

### 🧪 Local Development

```bash
# 1. Clone the repository
git clone https://github.com/princess12-crypto/Energy-for-Africa
cd Energy-for-Africa

# 2. Set up a virtual environment
python -m venv venv
# For Windows:
venv\Scripts\activate
# For Mac/Linux:
source venv/bin/activate

# 3. Install required packages
pip install -r requirements.txt

Environment Variables
Create a .env file in the root directory and add the following variables:

env
Copy
Edit

# MySQL Database Configuration
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=your_database_name


# Email SMTP Configuration
MAIL_SERVER=smtp.yourmail.com
MAIL_PORT=587
MAIL_USERNAME=your_email@example.com
MAIL_PASSWORD=your_email_password
MAIL_USE_TLS=True
On Railway, go to the Environment tab to set these variables securely.


👨‍💻 Author
Nkwo Celestine Justice
Full-Stack Web Developer
📍 Rivers State, Nigeria
📫 celestinejustice4@gmail.com
Call: 07032715779
School: University Of Port Harcourt
Occupation: Unique Student

🏁 Submission
This project was submitted for the Railway User Hackathon – August 2025. 
Energy for Africa is a professionally designed, full-stack web app built with Flask + MySQL. It features a contact form that stores user data in a Railway-hosted MySQL database and sends real-time confirmation emails using Brevo SMTP. Fully responsive, deploy-ready, and built with care for Africa’s energy vision.
# 4. Run the Flask app
python app.py
