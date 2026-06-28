# 🚀 Gig Worker Income Smoothing Platform

An AI-powered financial management platform designed to help gig workers achieve stable and predictable income through an innovative **Income Smoothing Algorithm**. The system records daily earnings, maintains a financial buffer, generates AI-driven insights, and integrates a Razorpay payment gateway for salary disbursement.

---

## 📖 Overview

Gig workers often experience fluctuating daily earnings due to inconsistent demand and working hours. This project provides a digital solution that smooths irregular income into a predictable virtual salary while maintaining a financial buffer.

The application is built using **Python Flask**, **PostgreSQL**, **Bootstrap**, and **Razorpay**, with analytics and AI-based financial recommendations.

---

## ✨ Features

* 🔐 User Registration & Login
* 👥 Worker Management
* 💰 Income Tracking
* 📈 Income Smoothing Algorithm
* 🏦 Buffer Ledger Management
* 📊 Analytics Dashboard
* 🤖 AI Financial Insights
* ⚠ AI Alert System
* 💳 Razorpay Payment Gateway Integration
* 📉 Charts & Financial Reports

---

## 🛠 Tech Stack

| Category        | Technology                   |
| --------------- | ---------------------------- |
| Backend         | Python, Flask                |
| Database        | PostgreSQL 17                |
| Frontend        | HTML5, CSS3, Bootstrap 5     |
| Charts          | Chart.js                     |
| Payment Gateway | Razorpay                     |
| AI Module       | Custom Recommendation Engine |
| Version Control | Git & GitHub                 |

---

## 📂 Project Structure

```
gig-worker-income-smoothing/

│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── workers.html
│   ├── income.html
│   ├── analytics.html
│   ├── login.html
│   ├── register.html
│   └── payment.html
│
├── gigapp.py
├── db.py
├── payment.py
├── financial_engine.py
├── ai_recommender.py
├── config.py
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/tharunmkt/gig-worker-income-smoothing.git

cd gig-worker-income-smoothing
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure PostgreSQL

Create a PostgreSQL database.

Example

```
gig_worker_db
```

Update the database credentials inside `config.py`.

### Run the Application

```bash
python gigapp.py
```

Open

```
http://127.0.0.1:5000
```

---

# 🧠 Income Smoothing Algorithm

### When Income > Target

```
Deposit = Actual Income − Target Income
Buffer = Buffer + Deposit
Virtual Salary = Target Income
```

### When Income < Target

```
Withdrawal = Minimum(Buffer, Shortage)
Virtual Salary = Actual Income + Withdrawal
Buffer = Buffer − Withdrawal
```

---

# 📊 Modules

### Authentication

* Login
* Registration
* Session Management

### Dashboard

* Worker Statistics
* Today's Income
* Virtual Salary
* Buffer Balance
* Health Score

### Worker Management

* Add Worker
* View Workers
* Store Platform Information

### Income Module

* Record Daily Income
* Income Smoothing
* Buffer Ledger Update

### Analytics

* Income Trends
* Platform Distribution
* AI Recommendations
* Health Analysis

### Payments

* Razorpay Order Creation
* Salary Payment
* Payment Success Handling

---

# 📸 Screenshots

Add screenshots here after uploading them.

Example

* Login Page
* Dashboard
* Worker Management
* Income Tracking
* Analytics Dashboard
* Razorpay Payment

---

# 📈 Future Enhancements

* Mobile Application
* UPI Auto Settlement
* Predictive Income Forecasting
* Multi-Platform Integration
* SMS & Email Notifications
* AI Chat Assistant
* Expense Tracking
* Admin Dashboard
* Worker Mobile Portal

---

# 📚 Academic Objectives

This project demonstrates

* Flask Web Development
* PostgreSQL Database Design
* Financial Algorithms
* Payment Gateway Integration
* Session Authentication
* AI Recommendation Systems
* Data Analytics
* Full Stack Development

---

# 👨‍💻 Author

**Tharun M K T**

Bachelor of Science: Computer Science (BSC.CS)

Project: Gig Worker Income Smoothing Platform

GitHub: https://github.com/tharunmkt

---

# 📜 License

This project is developed for academic and educational purposes.
