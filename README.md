# AI-Powered Patient Health Monitoring System

## Overview

The AI-Powered Patient Health Monitoring System is a Flask-based web application that enables healthcare staff to manage patient records and generate AI-powered health insights based on blood test parameters.

The application uses Google Gemini AI to analyze patient health metrics such as glucose, haemoglobin, and cholesterol levels and automatically generates health-risk summaries and dietary recommendations.

---

## Features

### Patient Management (CRUD)

* Create patient records
* View patient records
* Update patient information
* Delete patient records

### AI-Powered Health Analysis

* Automatic health-risk assessment
* Personalized dietary recommendations
* Gemini 2.5 Flash integration
* AI-generated health remarks stored in the database

### Data Validation

* Date of Birth validation
* Future date prevention
* Numeric value validation
* Negative value prevention

### Database Management

* SQLite database integration
* Automatic table creation
* Persistent patient record storage

---

## Technology Stack

### Backend

* Python
* Flask

### Database

* SQLite

### AI Service

* Google Gemini 2.5 Flash

### Frontend

* HTML
* CSS
* Jinja2 Templates

---

## Project Architecture

```text
User
  │
  ▼
Flask Web Application
  │
  ├── Form Validation
  │
  ├── SQLite Database
  │
  └── Gemini AI Analysis
          │
          ▼
    Health Recommendations
          │
          ▼
      Dashboard
```

---

## Database Schema

### Patients Table

| Column      | Type    | Description                  |
| ----------- | ------- | ---------------------------- |
| id          | INTEGER | Primary Key                  |
| full_name   | TEXT    | Patient Name                 |
| dob         | TEXT    | Date of Birth                |
| email       | TEXT    | Patient Email                |
| glucose     | REAL    | Glucose Level                |
| haemoglobin | REAL    | Haemoglobin Level            |
| cholesterol | REAL    | Cholesterol Level            |
| remarks     | TEXT    | AI Generated Health Analysis |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/health-monitoring-system.git
cd health-monitoring-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install flask google-genai
```

### Configure Gemini API Key

Windows:

```bash
set GEMINI_API_KEY=your_api_key
```

Linux/Mac:

```bash
export GEMINI_API_KEY=your_api_key
```

---

## Run Application

```bash
python app.py
```

Application will be available at:

```text
http://127.0.0.1:5000
```

---

## Application Workflow

1. User enters patient information.
2. Flask validates the submitted data.
3. Data is checked for invalid values.
4. Gemini AI receives blood test metrics.
5. AI generates a health-risk summary.
6. Record and AI remarks are stored in SQLite.
7. Results are displayed on the dashboard.

---

## Sample Input

```text
Name: John Doe
DOB: 1998-05-10
Email: john@example.com

Glucose: 145
Haemoglobin: 11.5
Cholesterol: 245
```

---

## Sample AI Output

```text
Elevated glucose and cholesterol levels may indicate increased metabolic and cardiovascular risk. Consider reducing sugar intake, increasing physical activity, and following a balanced diet while consulting a healthcare professional.
```

---

## Security and Validation

The application includes:

* Server-side validation
* Date validation
* Numeric validation
* Positive value enforcement
* Error handling for AI service failures
* Database transaction management

---

## Future Enhancements

* User Authentication
* Doctor Dashboard
* Patient Login Portal
* PDF Health Reports
* Email Notifications
* Health Trend Charts
* Appointment Scheduling
* Cloud Deployment (AWS/Azure/GCP)
* Predictive Disease Detection
* Electronic Health Record Integration

---

## Learning Outcomes

Through this project, the following concepts were implemented:

* Flask Web Development
* CRUD Operations
* SQLite Database Integration
* Form Validation
* RESTful Routing
* Prompt Engineering
* Gemini AI Integration
* Error Handling
* Backend Application Design

---
