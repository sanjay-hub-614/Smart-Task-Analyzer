# 🚀 Django Project Setup & Run Guide

This guide explains how to set up and run the Django project on your local machine.

---

## 📌 Prerequisites

Make sure you have the following installed:

- *Python 3.8+*
- *pip* (Python package manager)
- *virtualenv* (optional but recommended)
- *Git* (if cloning from a repository)

---

## 📁 1. Clone the Repository

```bash
git clone https://github.com/sanjay-hub-614/Smart-Task-Analyzer.git
cd Smart-Task-Analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

